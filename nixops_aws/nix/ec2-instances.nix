# { evalResources, zipAttrs, resourcesByType, ... }:
args@{ config, lib, uuid, name, ... }:

with lib;


let
  cfg = config.ec2Instances;
in
{
  imports = [ ./common-ec2-auth-options.nix ];

  options = {
    # reservationId = mkOption {
    #   default = "";
    #   type = types.str;
    #   description = "Reservation ID (set by NixOps)";
    # };

    # instanceIds = mkOption {
    #   default = [ ];
    #   type = types.listOf types.str;
    #   description = "List of allocated EC2 instance IDs (set by NixOps)";
    # };

    awsConfig = mkOption {
      default = { };
      example = {
        BlockDeviceMappings = [{ DeviceName = "/dev/sdh"; Ebs = { VolumeSize = 100; }; }];
        ImageId = "ami-abc12345";
        InstanceType = "t2.micro";
        KeyName = "my-key-pair";
        MaxCount = 1;
        MinCount = 1;
        SecurityGroupIds = [ "sg-1a2b3c4d" ];
        SubnetId = "subnet-6e7f829e";
      };
      type = types.attrs;
      description = "Extra configuration.";
    };
  }
  // (import ./common-ec2-options.nix { inherit lib; });

  config =
    mkIf true
      {
        _type = "ec2-instances";
      };

}


