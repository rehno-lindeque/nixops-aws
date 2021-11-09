#! /usr/bin/env nix-shell
#! nix-shell -i bash -p jq
curl --silent https://raw.githubusercontent.com/boto/botocore/develop/botocore/data/ec2/2016-11-15/service-2.json | jq -r '
.shapes as $shapes
| .operations as $operations
| "class '"$1"':
\(
[ $shapes["'"$1"'"]? // ($operations["'"$1"'"] | $shapes[.input.shape])
| (.required // []) as $required
| .members
| to_entries
| .[]
| .key as $k
| ($required | any(. == $k) | not) as $optional
|
"    \($k): \(if $optional then "Optional[\(.value.shape)]" else "\(.value.shape)" end)
        # \(.value.shape) = \(
          "Union[\n\(
          [ $shapes[.value.shape].enum
          | .[]
          | "        #     Literal[\"\(.)\"]"
          ]
          | join(",\n")
          )
        # ]"? // $shapes[.value.shape]? // ""
        )
        # \(.value | del(.shape) | del(.required) | del(.documentation) | del(.locationName))"
]
| join("\n")
)"
'

