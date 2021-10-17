{ config, lib, uuid, name, ... }:

with lib;


let
  cfg = config.awsSpotFleetRequest;

  launchSpecificationOptions = {
    options = {
      # TODO
    };
  };

  fleetLaunchTemplateSpecificationOptions = {
    options = {
      # launchTemplateId = mkOption {
      #   # default = ; # Optional
      #   # example = ;
      #   type = types.str;
      #   description = "The ID of the launch template. If you specify the template ID, you can't specify the template name.";
      # };

      launchTemplateName = mkOption {
        # default = ; # Optional
        # example = ;
        type = types.str;
        description = "The name of the launch template. If you specify the template name, you can't specify the template ID.";
      };

      version = mkOption {
        # default = ; # Optional
        # example = ;
        type = types.str;
        description = ''
          The launch template version number, <literal>"$Latest"</literal>, or <literal>"$Default"</literal>.
          If the value is <literal>"$Latest"</literal>, Amazon EC2 uses the latest version of the launch template.
          If the value is <literal>"$Default"</literal>, Amazon EC2 uses the default version of the launch template.
        '';
      };
    };
  };

  launchTemplateOverridesOptions = {
    options = {
      spotPrice = mkOption {
        default = null;
        # example = ;
        type = with types; nullOr str;
        description = "The maximum price per unit hour that you are willing to pay for a Spot Instance.";
      };

      subnetId = mkOption {
        default = null;
        # example = ;
        type = with types; nullOr str;
        # description = "The ID of the subnet in which to launch the instances.";
      };

      availabilityZone = mkOption {
        default = null;
        # example = ;
        type = with types; nullOr str;
        description = "The Availability Zone in which to launch the instances.";
      };

      weightedCapacity = mkOption {
        default = null;
        # example = ;
        type = with types; nullOr float;
        description = "The number of units provided by the specified instance type.";
      };

      priority = mkOption {
        default = null;
        # example = ;
        type = with types; nullOr float;
        description = ''
          The priority for the launch template override. The highest priority is launched first.
          If <code>OnDemandAllocationStrategy</code> is set to <literal>"prioritized"</literal>, Spot Fleet uses priority to determine which launch template override to use first in fulfilling On-Demand capacity.
          If the Spot <code>AllocationStrategy</code> is set to <literal>"capacityOptimizedPrioritized"</literal>, Spot Fleet uses priority on a best-effort basis to determine which launch template override to use in fulfilling Spot capacity, but optimizes for capacity first.
          Valid values are whole numbers starting at <literal>0</literal>. The lower the number, the higher the priority. If no number is set, the launch template override has the lowest priority. You can set the same priority for different launch template overrides.
        '';
      };

      # Common EC2 instance options
      instanceType = mkOption {
        default = null;
        # example = ;
        type = with types; nullOr str;
        description = "The instance type.";
      };
    };
  };

  launchTemplateConfigOptions = {
    options = {
      launchTemplateSpecification = mkOption {
        # default = ; # Optional
        # example = ;
        type = types.submodule fleetLaunchTemplateSpecificationOptions;
        description = "The launch template.";
      };

      overrides = mkOption {
        default = [ ]; # Optional
        example = [
          {
            instanceType = "m1.small";
            weightedCapacity = 1.;
          }
          {
            instanceType = "m3.medium";
            weightedCapacity = 1.;
          }
          {
            instanceType = "m1.medium";
            weightedCapacity = 1.;
          }
        ];
        type = with types; listOf (types.submodule launchTemplateOverridesOptions);
        description = "Any parameters that you specify override the same parameters in the launch template.";
      };
    };
  };
in
{
  imports = [ ./common-ec2-auth-options.nix ];

  options = {

    spotFleetRequestId = mkOption {
      default = "";
      type = types.str;
      description = "Spot fleet request ID (set by NixOps)";
    };

    # allocationStrategy = mkOption {
    #   # default = ; # Optional
    #   # example = ;
    #   type =
    #     types.enum [
    #       "lowestPrice"
    #       "diversified"
    #       "capacityOptimized"
    #       "capacityOptimizedPrioritized"
    #     ];
    #   # description = "<p>Indicates how to allocate the target Spot Instance capacity across the Spot Instance pools specified by the Spot Fleet request.</p> <p>If the allocation strategy is <code>lowestPrice</code>, Spot Fleet launches instances from the Spot Instance pools with the lowest price. This is the default allocation strategy.</p> <p>If the allocation strategy is <code>diversified</code>, Spot Fleet launches instances from all the Spot Instance pools that you specify.</p> <p>If the allocation strategy is <code>capacityOptimized</code> (recommended), Spot Fleet launches instances from Spot Instance pools with optimal capacity for the number of instances that are launching. To give certain instance types a higher chance of launching first, use <code>capacityOptimizedPrioritized</code>. Set a priority for each instance type by using the <code>Priority</code> parameter for <code>LaunchTemplateOverrides</code>. You can assign the same priority to different <code>LaunchTemplateOverrides</code>. EC2 implements the priorities on a best-effort basis, but optimizes for capacity first. <code>capacityOptimizedPrioritized</code> is supported only if your Spot Fleet uses a launch template. Note that if the <code>OnDemandAllocationStrategy</code> is set to <code>prioritized</code>, the same priority is applied when fulfilling On-Demand capacity.</p>";
    # };

    # OnDemandAllocationStrategy = mkOption {
    #   # OnDemandAllocationStrategy
    #   # default = ; # Optional
    #   # example = ;
    #   type =
    #     types.enum [
    #       "lowestPrice"
    #       "prioritized"
    #     ];
    #   # description = "<p>The order of the launch template overrides to use in fulfilling On-Demand capacity. If you specify <code>lowestPrice</code>, Spot Fleet uses price to determine the order, launching the lowest price first. If you specify <code>prioritized</code>, Spot Fleet uses the priority that you assign to each Spot Fleet launch template override, launching the highest priority first. If you do not specify a value, Spot Fleet defaults to <code>lowestPrice</code>.</p>";

    # SpotMaintenanceStrategies = mkOption {
    #   # SpotMaintenanceStrategies
    #   # default = ; # Optional
    #   # example = ;
    #   type =
    #       types.submodule # {"type":"structure","members":{"CapacityRebalance":{"shape":"SpotCapacityRebalance","documentation":"<p>The strategy to use when Amazon EC2 emits a signal that your Spot Instance is at an elevated risk of being interrupted.</p>","locationName":"capacityRebalance"}},"documentation":"<p>The strategies for managing your Spot Instances that are at an elevated risk of being interrupted.</p>"};
    #   # description = "<p>The strategies for managing your Spot Instances that are at an elevated risk of being interrupted.</p>";

    # ClientToken = mkOption {
    #   # String
    #   # default = ; # Optional
    #   # example = ;
    #   type =
    #     types.string;
    #   # description = "<p>A unique, case-sensitive identifier that you provide to ensure the idempotency of your listings. This helps to avoid duplicate listings. For more information, see <a href="https://docs.aws.amazon.com/AWSEC2/latest/APIReference/Run_Instance_Idempotency.html">Ensuring Idempotency</a>.</p>";

    # ExcessCapacityTerminationPolicy = mkOption {
    #   # ExcessCapacityTerminationPolicy
    #   # default = ; # Optional
    #   # example = ;
    #   type =
    #     types.enum [
    #       "noTermination"
    #       "default"
    #     ];
    #   # description = "<p>Indicates whether running Spot Instances should be terminated if you decrease the target capacity of the Spot Fleet request below the current size of the Spot Fleet.</p>";

    iamFleetRole = mkOption {
      # example = "rolename"; # TODO
      type = types.str;
      description = ''
        The Amazon Resource Name (ARN) of an Identity and Access Management
        (IAM) role that grants the Spot Fleet the permission to request,
        launch, terminate, and tag instances on your behalf.

        Spot Fleet can terminate Spot Instances on your behalf when you cancel
        its Spot Fleet request or when the Spot Fleet request expires, if you
        set <code>TerminateInstancesWithExpiration</code>.
      '';
    };

    # launchSpecifications = mkOption {
    #   # default = ; # Optional
    #   # example = ;
    #   type = with types; listOf (submodule launchSpecificationOptions);
    #   description = "<p>The launch specifications for the Spot Fleet request. If you specify <code>LaunchSpecifications</code>, you can't specify <code>LaunchTemplateConfigs</code>. If you include On-Demand capacity in your request, you must use <code>LaunchTemplateConfigs</code>.</p>";
    # };

    launchTemplateConfigs = mkOption
      {
        type = with types; listOf (submodule launchTemplateConfigOptions);
        description = ''
          The launch template and overrides. If you specify <code>LaunchTemplateConfigs</code>, you can't specify <code>LaunchSpecifications</code>. If you include On-Demand capacity in your request, you must use <code>LaunchTemplateConfigs</code>.
        '';
      };

    spotPrice = mkOption {
      # default = ; # Optional
      # example = ;
      type = with types; nullOr str;
      description = ''
        The maximum price per unit hour that you are willing to pay for a Spot Instance. The default is the On-Demand price.
      '';
    };

    # targetCapacity = mkOption {
    #   # default = ; # Required
    #   # example = ;
    #   type =
    #     types.int;
    #   # description = "<p>The number of units to request for the Spot Fleet. You can choose to set the target capacity in terms of instances or a performance characteristic that is important to your application workload, such as vCPUs, memory, or I/O. If the request type is <code>maintain</code>, you can specify a target capacity of 0 and add capacity later.</p>";
    # };

    # onDemandTargetCapacity = mkOption {
    #   # default = ; # Optional
    #   # example = ;
    #   type =
    #     types.int;
    #   # description = "<p>The number of On-Demand units to request. You can choose to set the target capacity in terms of instances or a performance characteristic that is important to your application workload, such as vCPUs, memory, or I/O. If the request type is <code>maintain</code>, you can specify a target capacity of 0 and add capacity later.</p>";
    # };

    # onDemandMaxTotalPrice = mkOption {
    #   # default = ; # Optional
    #   # example = ;
    #   type =
    #     types.string;
    #   # description = "<p>The maximum amount per hour for On-Demand Instances that you're willing to pay. You can use the <code>onDemandMaxTotalPrice</code> parameter, the <code>spotMaxTotalPrice</code> parameter, or both parameters to ensure that your fleet cost does not exceed your budget. If you set a maximum price per hour for the On-Demand Instances and Spot Instances in your request, Spot Fleet will launch instances until it reaches the maximum amount you're willing to pay. When the maximum amount you're willing to pay is reached, the fleet stops launching instances even if it hasn’t met the target capacity.</p>";
    # };

    spotMaxTotalPrice = mkOption {
      # default = ; # Optional
      # example = ;
      type = with types; nullOr str;
      description = "The maximum amount per hour for Spot Instances that you're willing to pay. You can use the <code>spotdMaxTotalPrice</code> parameter, the <code>onDemandMaxTotalPrice</code> parameter, or both parameters to ensure that your fleet cost does not exceed your budget. If you set a maximum price per hour for the On-Demand Instances and Spot Instances in your request, Spot Fleet will launch instances until it reaches the maximum amount you're willing to pay. When the maximum amount you're willing to pay is reached, the fleet stops launching instances even if it hasn’t met the target capacity.";
    };

    # terminateInstancesWithExpiration = mkOption {
    #   # default = ; # Optional
    #   # example = ;
    #   type = types.boolean;
    #   # description = "<p>Indicates whether running Spot Instances are terminated when the Spot Fleet request expires.</p>";
    #   # extra = {};
    # };

    type = mkOption {
      default = "maintain";
      example = "request";
      type =
        types.enum [
          "request"
          "maintain"
          # "instant" # instant is listed but is not used by Spot Fleet.
        ];
      description = ''
        The type of request. Indicates whether the Spot Fleet only requests
        the target capacity or also attempts to maintain it. When this
        value is <code>request</code>, the Spot Fleet only places the
        required requests. It does not attempt to replenish Spot Instances if
        capacity is diminished, nor does it submit requests in alternative Spot
        pools if capacity is not available. When this value is
        <code>maintain</code>, the Spot Fleet maintains the target capacity.
        The Spot Fleet places the required requests to meet capacity and
        automatically replenishes any interrupted instances.
      '';
    };

    # ValidFrom = mkOption {
    #   # DateTime
    #   # default = ; # Optional
    #   # example = ;
    #   type =
    #     # Unknown type timestamp;
    #   # description = "<p>The start date and time of the request, in UTC format (<i>YYYY</i>-<i>MM</i>-<i>DD</i>T<i>HH</i>:<i>MM</i>:<i>SS</i>Z). By default, Amazon EC2 starts fulfilling the request immediately.</p>";
    # };

    # ValidUntil = mkOption {
    #   # DateTime
    #   # default = ; # Optional
    #   # example = ;
    #   type =
    #     # Unknown type timestamp;
    #   # description = "<p>The end date and time of the request, in UTC format (<i>YYYY</i>-<i>MM</i>-<i>DD</i>T<i>HH</i>:<i>MM</i>:<i>SS</i>Z). After the end date and time, no new Spot Instance requests are placed or able to fulfill the request. If no value is specified, the Spot Fleet request remains until you cancel it.</p>";
    # };

    # ReplaceUnhealthyInstances = mkOption {
    #   # default = ; # Optional
    #   # example = ;
    #   type =
    #     types.boolean;
    #   # description = "Indicates whether Spot Fleet should replace unhealthy instances.";
    #   # extra = {};
    # };

    # InstanceInterruptionBehavior = mkOption {
    #   # InstanceInterruptionBehavior
    #   # default = ; # Optional
    #   # example = ;
    #   type =
    #     types.enum [
    #       "hibernate"
    #       "stop"
    #       "terminate"
    #     ];
    #   # description = "<p>The behavior when a Spot Instance is interrupted. The default is <code>terminate</code>.</p>";
    # };

    # LoadBalancersConfig = mkOption {
    #   # LoadBalancersConfig
    #   # default = ; # Optional
    #   # example = ;
    #   type =
    #       types.submodule ...
    #   # description = "<p>One or more Classic Load Balancers and target groups to attach to the Spot Fleet request. Spot Fleet registers the running Spot Instances with the specified Classic Load Balancers and target groups.</p> <p>With Network Load Balancers, Spot Fleet cannot register instances that have the following instance types: C1, CC1, CC2, CG1, CG2, CR1, CS1, G1, G2, HI1, HS1, M1, M2, M3, and T1.</p>";
    # };

    # InstancePoolsToUseCount = mkOption {
    #   # Integer
    #   # default = ; # Optional
    #   # example = ;
    #   type =
    #     types.int;
    #   # description = "<p>The number of Spot pools across which to allocate your target Spot capacity. Valid only when Spot <b>AllocationStrategy</b> is set to <code>lowest-price</code>. Spot Fleet selects the cheapest Spot pools and evenly allocates your target Spot capacity across the number of Spot pools that you specify.</p> <p>Note that Spot Fleet attempts to draw Spot Instances from the number of pools that you specify on a best effort basis. If a pool runs out of Spot capacity before fulfilling your target capacity, Spot Fleet will continue to fulfill your request by drawing from the next cheapest pool. To ensure that your target capacity is met, you might receive Spot Instances from more than the number of pools that you specified. Similarly, if most of the pools have no Spot capacity, you might receive your full target capacity from fewer than the number of pools that you specified.</p>";
    # };

    awsConfig = mkOption {
      default = {};
      example = {
        SpotFleetRequestConfig = {
          AllocationStrategy = "lowestPrice";
        };
      };
      type = types.attrs;
      description = "Extra configuration.";
    };
  }
  // (import ./common-ec2-options.nix { inherit lib; });

  config =
    mkIf
      # (if cfg.launchSpecifications ?? || cfg then true else throw "\nFailed assertion: ${message}")
      true
      {
        _type = "aws-spot-fleet-request";
      };

}


