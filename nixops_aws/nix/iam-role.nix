{ config, lib, uuid, name, ... }:

with lib;

let
  cfg = config.iamRole;
  stateReference = { resource, field, reftype }: {
    _type = "reference-type";
    _reftype = reftype.name;
    inherit resource field;
  };
in
{
  options = {

    name = mkOption {
      default = "charon-${uuid}-${name}";
      type = types.str;
      description = "Name of the IAM role.";
    };

    accessKeyId = mkOption {
      type = types.str;
      default = "";
      description = "The AWS Access Key ID.";
    };

    policy = mkOption {
      type = types.str;
      description = "The IAM policy definition (in JSON format).";
    };

    assumeRolePolicy = mkOption {
      type = types.str;
      description = "The IAM AssumeRole policy definition (in JSON format). Empty string (default) uses the existing Assume Role Policy.";
      default = "";
    };

  } // import ./common-ec2-options.nix { inherit lib; };

  config =
    mkIf
      # (if cfg.launchSpecifications ?? || cfg then true else throw "\nFailed assertion: ${message}")
      true
      {
        _type = "iam-role";
      };
}
