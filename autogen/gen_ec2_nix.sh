#! /usr/bin/env nix-shell
#! nix-shell -i bash -p jq
curl --silent https://raw.githubusercontent.com/boto/botocore/develop/botocore/data/ec2/2016-11-15/service-2.json | jq -r '
.shapes as $shapes
|
def printshape($whitespace):
  def printstruct($whitespace):
    # "\($whitespace){\n\($whitespace + "  ")\(
    #     [ .members
    #     | to_entries
    #     | .[]
    #     | "\(.key) =\n\(.value.shape | printshape($whitespace + "    "))"
    #     ] | join("\n\($whitespace + "  ")")
    #   )\n\($whitespace)}"
    "\($whitespace)types.submodule # \(.)"
    ;
  def printenum($whitespace):
    "\($whitespace)types.enum [\n\([ .enum[] | "\($whitespace)  \"\(.)\"\n" ] | join(""))\($whitespace)]"
    ;
  def printtype($whitespace):
  if (. | has("enum")) then
      (. | printenum($whitespace))
    elif .type == "list" then
      "\($whitespace)with types; listOf # \(.member.shape)\n\(.member.shape | printshape($whitespace + "  "))"
    elif .type == "structure" then
      (. | printstruct($whitespace + "  "))
    elif .type == "string" then
      "\($whitespace)types.string"
    elif .type == "boolean" then
      "\($whitespace)types.boolean"
    elif .type == "integer" then
      "\($whitespace)types.int"
    else
      "\($whitespace)# Unknown type \(.type)"
    end
    ;
  ($shapes[.] | printtype($whitespace))? // "\($whitespace)# Error: shape \(.) \($shapes[.]?)"
  # ($shapes[.] | printtype($whitespace))
  ;
.operations as $operations
| "# '"$1"'
\(
[ $shapes["'"$1"'"]? // ($operations["'"$1"'"] | $shapes[.input.shape])
| (.required // []) as $required
| .members
| to_entries
| .[]
| .key as $k
| ($required | any(. == $k) | not) as $optional
| .value
|
"  \($k) = mkOption {
    # \(.shape)
    # default = ; # \(if $optional then "Optional" else "Required" end)
    # example = ;
    type =\n\((.shape | printshape("      "))?);
    # description = \"\(.documentation)\";
    # extra = \(. | del(.shape) | del(.required) | del(.documentation) | del(.locationName));"
]
| join("\n\n")
)"
'

