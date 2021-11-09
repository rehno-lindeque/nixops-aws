# Configuration specific to the EC2 backend.

{ config, pkgs, lib, utils, ... }:

with utils;
with lib;
with import ./lib.nix lib;

let
  cfg = config.deployment.ec2Target;

  instanceOptions = {
    options.instanceId = mkOption {
      default = null;
      example = "i-00000000000000000";
      type = with types; nullOr (either str (resource "ec2-instances"));
      apply = x: if x == null || builtins.isString x then x else "res-${x._name}";
      description = ''
        EC2 instance to use as the target of this deployment.
      '';
    };
  };

  spotRequestOptions = {
    options.spotRequestId = mkOption {
      default = null;
      example = "sir-00000000";
      type = with types; nullOr (either str (resource "ec2-spot-request"));
      apply = x: if x == null || builtins.isString x then x else "res-${x._name}";
      description = ''
        EC2 spot request to use as the target of this deployment.
      '';
    };
  };

  spotFleetRequestOptions = {
    options.spotFleetRequestId = mkOption {
      default = null;
      example = "sfr-00000000-0000-0000-0000-000000000000";
      # type = with types; either str (resource "ec2-spot-fleet-request");
      type = with types; nullOr (either str (resource "aws-spot-fleet"));
      apply = x: if x == null || builtins.isString x then x else "res-${x._name}";
      description = ''
        EC2 spot fleet request to use as the target of this deployment.
      '';
    };
  };

in

{
  options.deployment.ec2 = {
    target = mkOption {
      example = literalExample ''
       { instanceId = resources.instance."node-1"; }
      '';
      # TODO: check type is oneOf submodules
      # type = with types; oneOf [
      #   (submodule instanceOptions)
      #   (submodule spotRequestOptions)
      #   (submodule spotFleetRequestOptions)
      # ];
      # type = with types; addCheck (oneOf [
      #   (submodule instanceOptions)
      #   (submodule spotRequestOptions)
      #   (submodule spotFleetRequestOptions)
      # ]) (x: x ? instanceId || x ? spotRequestId || x ? spotFleetRequestId);
      # type = with types; submodule spotFleetRequestOptions;
      type = with types; submoduleWith {
        modules = [
          instanceOptions
          spotRequestOptions
          spotFleetRequestOptions
        ];
      };
      # apply = x: lib.traceSeqN 2 x;
      # type = with types; oneOf [
      #   str
      #   (resource "ec2-instance")
      #   (resource "ec2-spot-request")
      #   (resource "aws-spot-fleet")
      # ];
      # apply = x: if builtins.isString x then x else "res-${x._type}-${x._name}";
      description = ''
        EC2 target to use when provisioning this machine.
      '';
    };

    privateKey = mkOption {
      default = "";
      example = "/home/alice/.ssh/id_rsa-my-keypair";
      type = types.str;
      description = ''
        Path of the SSH private key file corresponding with
        <option>deployment.ec2.keyPair</option>.  NixOps will use this
        private key if set; otherwise, the key must be findable by SSH
        through its normal mechanisms (e.g. it should be listed in
        <filename>~/.ssh/config</filename> or added to the
        <command>ssh-agent</command>).
      '';
    };
  };


  config = mkIf (config.deployment.targetEnv == "ec2-target") {
    # deployment.ec2Target = {
    # };
  };
}
