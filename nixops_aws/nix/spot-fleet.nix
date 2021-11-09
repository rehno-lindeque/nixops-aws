{ config, lib, uuid, name, ... }:

with import ./lib.nix lib;
with lib;

let
  cfg = config.awsSpotFleet;

  ebsBlockDeviceOptions = {
    options = {
      deleteOnTermination = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.bool;
        description = ''
          Undocumented
        '';
      };
      encrypted = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.bool;
        description = ''
          Undocumented
        '';
      };
      iops = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.int;
        description = ''
          Undocumented
        '';
      };
      kmsKeyId = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      outpostArn = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      snapshotId = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      throughput = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.int;
        description = ''
          Undocumented
        '';
      };
      volumeSize = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.int;
        description = ''
          Undocumented
        '';
      };
      volumeType = mkOption {
        default = null;
        # example = ;
        type = types.nullOr (types.enum [ "gp2" "gp3" "io1" "io2" "sc1" "st1" "standard" ]);
        description = ''
          Undocumented
        '';
      };
    };
  };
  blockDeviceMappingOptions = {
    options = {
      deviceName = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      ebs = mkOption {
        default = null;
        # example = ;
        type = types.nullOr (types.submodule ebsBlockDeviceOptions);
        description = ''
          Undocumented
        '';
      };
      noDevice = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      virtualName = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
    };
  };
  iamInstanceProfileSpecificationOptions = {
    options = {
      arn = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      name = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
    };
  };
  spotFleetMonitoringOptions = {
    options = {
      enabled = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.bool;
        description = ''
          Undocumented
        '';
      };
    };
  };
  ipv4PrefixSpecificationOptions = {
    options = {
      ipv4Prefix = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
    };
  };
  instanceIpv6AddressOptions = {
    options = {
      ipv6Address = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
    };
  };
  ipv6PrefixSpecificationOptions = {
    options = {
      ipv6Prefix = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
    };
  };
  privateIpAddressSpecificationOptions = {
    options = {
      primary = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.bool;
        description = ''
          Undocumented
        '';
      };
      privateIpAddress = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
    };
  };
  instanceNetworkInterfaceSpecificationOptions = {
    options = {
      associateCarrierIpAddress = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.bool;
        description = ''
          Undocumented
        '';
      };
      associatePublicIpAddress = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.bool;
        description = ''
          Undocumented
        '';
      };
      deleteOnTermination = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.bool;
        description = ''
          Undocumented
        '';
      };
      description = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      deviceIndex = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.int;
        description = ''
          Undocumented
        '';
      };
      groups = mkOption {
        default = [ ];
        example = [
          # Undocumented
        ];
        type = types.nullOr (types.listOf types.str);
        description = ''
          Undocumented
        '';
      };
      interfaceType = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      ipv4PrefixCount = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.int;
        description = ''
          Undocumented
        '';
      };
      ipv4Prefixes = mkOption {
        default = [ ];
        example = [
          # Undocumented
        ];
        type = types.nullOr (types.listOf (types.submodule ipv4PrefixSpecificationOptions));
        description = ''
          Undocumented
        '';
      };
      ipv6AddressCount = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.int;
        description = ''
          Undocumented
        '';
      };
      ipv6Addresses = mkOption {
        default = [ ];
        example = [
          # Undocumented
        ];
        type = types.nullOr (types.listOf (types.submodule instanceIpv6AddressOptions));
        description = ''
          Undocumented
        '';
      };
      ipv6PrefixCount = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.int;
        description = ''
          Undocumented
        '';
      };
      ipv6Prefixes = mkOption {
        default = [ ];
        example = [
          # Undocumented
        ];
        type = types.nullOr (types.listOf (types.submodule ipv6PrefixSpecificationOptions));
        description = ''
          Undocumented
        '';
      };
      networkCardIndex = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.int;
        description = ''
          Undocumented
        '';
      };
      networkInterfaceId = mkOption {
        default = null;
        # example = ;
        type = types.uniq (types.nullOr (types.either types.str (resource "vpc-network-interface")));
        apply = x: if (builtins.isString x || builtins.isNull x) then x else "res-" + x._name + "." + x._type + ".networkInterfaceId";
        description = ''
          Undocumented
        '';
      };
      privateIpAddress = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      privateIpAddresses = mkOption {
        default = [ ];
        example = [
          # Undocumented
        ];
        type = types.nullOr (types.listOf (types.submodule privateIpAddressSpecificationOptions));
        description = ''
          Undocumented
        '';
      };
      secondaryPrivateIpAddressCount = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.int;
        description = ''
          Undocumented
        '';
      };
      subnetId = mkOption {
        default = null;
        # example = ;
        type = types.uniq (types.nullOr (types.either types.str (resource "vpc-subnet")));
        apply = x: if (builtins.isString x || builtins.isNull x) then x else "res-" + x._name + "." + x._type + ".subnetId";
        description = ''
          Undocumented
        '';
      };
    };
  };
  spotPlacementOptions = {
    options = {
      availabilityZone = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      groupName = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      tenancy = mkOption {
        default = null;
        # example = ;
        type = types.nullOr (types.enum [ "dedicated" "default" "host" ]);
        description = ''
          Undocumented
        '';
      };
    };
  };
  groupIdentifierOptions = {
    options = {
      groupId = mkOption {
        default = null;
        # example = ;
        type = types.uniq (types.nullOr (types.either types.str (resource "ec2-security-groups")));
        apply = x: if (builtins.isString x || builtins.isNull x) then x else "res-" + x._name + "." + x._type + ".groupId";
        description = ''
          Undocumented
        '';
      };
      groupName = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
    };
  };
  spotFleetLaunchSpecificationOptions = {
    options = {
      addressingType = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      blockDeviceMappings = mkOption {
        default = [ ];
        example = [
          # Undocumented
        ];
        type = types.nullOr (types.listOf (types.submodule blockDeviceMappingOptions));
        description = ''
          Undocumented
        '';
      };
      ebsOptimized = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.bool;
        description = ''
          Undocumented
        '';
      };
      iamInstanceProfile = mkOption {
        default = null;
        # example = ;
        type = types.nullOr (types.submodule iamInstanceProfileSpecificationOptions);
        description = ''
          Undocumented
        '';
      };
      imageId = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      instanceType = mkOption {
        default = null;
        # example = ;
        type = types.str;
        description = ''
          Undocumented
        '';
      };
      kernelId = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      keyName = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      monitoring = mkOption {
        default = null;
        # example = ;
        type = types.nullOr (types.submodule spotFleetMonitoringOptions);
        description = ''
          Undocumented
        '';
      };
      networkInterfaces = mkOption {
        default = [ ];
        example = [
          # Undocumented
        ];
        type = types.nullOr (types.listOf (types.submodule instanceNetworkInterfaceSpecificationOptions));
        description = ''
          Undocumented
        '';
      };
      placement = mkOption {
        default = null;
        # example = ;
        type = types.nullOr (types.submodule spotPlacementOptions);
        description = ''
          Undocumented
        '';
      };
      ramdiskId = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      securityGroups = mkOption {
        default = [ ];
        example = [
          # Undocumented
        ];
        type = types.nullOr (types.listOf (types.submodule groupIdentifierOptions));
        description = ''
          Undocumented
        '';
      };
      spotPrice = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      subnetId = mkOption {
        default = null;
        # example = ;
        type = types.uniq (types.nullOr (types.either types.str (resource "vpc-subnet")));
        apply = x: if (builtins.isString x || builtins.isNull x) then x else "res-" + x._name + "." + x._type + ".subnetId";
        description = ''
          Undocumented
        '';
      };
      userData = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      weightedCapacity = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.float;
        description = ''
          Undocumented
        '';
      };
    };
  };
  fleetLaunchTemplateSpecificationOptions = {
    options = {
      launchTemplateId = mkOption {
        default = null;
        # example = ;
        type = types.uniq (types.nullOr (types.either types.str (resource "ec2-launch-template")));
        apply = x: if (builtins.isString x || builtins.isNull x) then x else "res-" + x._name + "." + x._type + ".templateId";
        description = ''
          The ID of the launch template. If you specify the template ID, you can't specify the template name.
        '';
      };
      launchTemplateName = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
      version = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
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
      availabilityZone = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          The Availability Zone in which to launch the instances.
        '';
      };
      instanceType = mkOption {
        default = null;
        # example = ;
        type = types.str;
        description = ''
          The instance type.
        '';
      };
      priority = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.float;
        description = ''
          The priority for the launch template override. The highest priority is launched first.
          If <code>OnDemandAllocationStrategy</code> is set to <literal>"prioritized"</literal>, Spot Fleet uses priority to determine which launch template override to use first in fulfilling On-Demand capacity.
          If the Spot <code>AllocationStrategy</code> is set to <literal>"capacityOptimizedPrioritized"</literal>, Spot Fleet uses priority on a best-effort basis to determine which launch template override to use in fulfilling Spot capacity, but optimizes for capacity first.
          Valid values are whole numbers starting at <literal>0</literal>. The lower the number, the higher the priority. If no number is set, the launch template override has the lowest priority. You can set the same priority for different launch template overrides.
        '';
      };
      spotPrice = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          The maximum price per unit hour that you are willing to pay for a Spot Instance.
        '';
      };
      subnetId = mkOption {
        default = null;
        # example = ;
        type = types.uniq (types.nullOr (types.either types.str (resource "vpc-subnet")));
        apply = x: if (builtins.isString x || builtins.isNull x) then x else "res-" + x._name + "." + x._type + ".subnetId";
        description = ''
          The ID of the subnet in which to launch the instances.
        '';
      };
      weightedCapacity = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.float;
        description = ''
          The number of units provided by the specified instance type.
        '';
      };
    };
  };
  launchTemplateConfigOptions = {
    options = {
      launchTemplateSpecification = mkOption {
        default = null;
        # example = ;
        type = types.nullOr (types.submodule fleetLaunchTemplateSpecificationOptions);
        description = ''
          The launch template.
        '';
      };
      overrides = mkOption {
        default = [ ];
        example = [
          {
            instanceType = "m1.small";
            weightedCapacity = 1.0;
          }
          {
            instanceType = "m3.medium";
            weightedCapacity = 1.0;
          }
          {
            instanceType = "m1.medium";
            weightedCapacity = 1.0;
          }
        ];
        type = types.nullOr (types.listOf (types.submodule launchTemplateOverridesOptions));
        description = ''
          Any parameters that you specify override the same parameters in the launch template.
        '';
      };
    };
  };
  classicLoadBalancerOptions = {
    options = {
      name = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
    };
  };
  classicLoadBalancersConfigOptions = {
    options = {
      classicLoadBalancers = mkOption {
        default = [ ];
        example = [
          # Undocumented
        ];
        type = types.nullOr (types.listOf (types.submodule classicLoadBalancerOptions));
        description = ''
          Undocumented
        '';
      };
    };
  };
  targetGroupOptions = {
    options = {
      arn = mkOption {
        default = null;
        # example = ;
        type = types.nullOr types.str;
        description = ''
          Undocumented
        '';
      };
    };
  };
  targetGroupsConfigOptions = {
    options = {
      targetGroups = mkOption {
        default = [ ];
        example = [
          # Undocumented
        ];
        type = types.nullOr (types.listOf (types.submodule targetGroupOptions));
        description = ''
          Undocumented
        '';
      };
    };
  };
  loadBalancersConfigOptions = {
    options = {
      classicLoadBalancersConfig = mkOption {
        default = null;
        # example = ;
        type = types.nullOr (types.submodule classicLoadBalancersConfigOptions);
        description = ''
          Undocumented
        '';
      };
      targetGroupsConfig = mkOption {
        default = null;
        # example = ;
        type = types.nullOr (types.submodule targetGroupsConfigOptions);
        description = ''
          Undocumented
        '';
      };
    };
  };
  spotCapacityRebalanceOptions = {
    options = {
      replacementStrategy = mkOption {
        default = null;
        # example = ;
        type = types.nullOr (types.enum [ "launch" ]);
        description = ''
          Undocumented
        '';
      };
    };
  };
  spotMaintenanceStrategiesOptions = {
    options = {
      capacityRebalance = mkOption {
        default = null;
        # example = ;
        type = types.nullOr (types.submodule spotCapacityRebalanceOptions);
        description = ''
          Undocumented
        '';
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
      description = ''
        Spot fleet request ID (set by NixOps)
      '';
    };
    iamFleetRole = mkOption {
      # example = ;
      type = types.either types.str (resource "iam-role");
      apply = x: if (builtins.isString x) then x else "res-" + x._name + "." + x._type + ".arn";
      description = ''
        The Amazon Resource Name (ARN) of an Identity and Access Management
        (IAM) role that grants the Spot Fleet the permission to request,
        launch, terminate, and tag instances on your behalf.

        Spot Fleet can terminate Spot Instances on your behalf when you cancel
        its Spot Fleet request or when the Spot Fleet request expires, if you
        set <code>TerminateInstancesWithExpiration</code>.
      '';
    };
    targetCapacity = mkOption {
      # example = ;
      type = types.int;
      description = ''
        The number of units to request for the Spot Fleet. You can choose to set the target capacity in terms of instances or a performance characteristic that is important to your application workload, such as vCPUs, memory, or I/O. If the request type is <code>maintain</code>, you can specify a target capacity of 0 and add capacity later.
      '';
    };
    allocationStrategy = mkOption {
      default = null;
      # example = ;
      type = types.nullOr (types.enum [ "capacityOptimized" "capacityOptimizedPrioritized" "diversified" "lowestPrice" ]);
      description = ''
        Indicates how to allocate the target Spot Instance capacity across the Spot Instance pools specified by the Spot Fleet request.
        If the allocation strategy is <code>lowestPrice</code>, Spot Fleet launches instances from the Spot Instance pools with the lowest price. This is the default allocation strategy.
        If the allocation strategy is <code>diversified</code>, Spot Fleet launches instances from all the Spot Instance pools that you specify.
        If the allocation strategy is <code>capacityOptimized</code> (recommended), Spot Fleet launches instances from Spot Instance pools with optimal capacity for the number of instances that are launching. To give certain instance types a higher chance of launching first, use <code>capacityOptimizedPrioritized</code>. Set a priority for each instance type by using the <code>Priority</code> parameter for <code>LaunchTemplateOverrides</code>. You can assign the same priority to different <code>LaunchTemplateOverrides</code>. EC2 implements the priorities on a best-effort basis, but optimizes for capacity first. <code>capacityOptimizedPrioritized</code> is supported only if your Spot Fleet uses a launch template. Note that if the <code>OnDemandAllocationStrategy</code> is set to <code>prioritized</code>, the same priority is applied when fulfilling On-Demand capacity.
      '';
    };
    excessCapacityTerminationPolicy = mkOption {
      default = null;
      # example = ;
      type = types.nullOr (types.enum [ "default" "noTermination" ]);
      description = ''
        Indicates whether running Spot Instances should be terminated if you decrease the target capacity of the Spot Fleet request below the current size of the Spot Fleet.
      '';
    };
    fulfilledCapacity = mkOption {
      default = null;
      # example = ;
      type = types.nullOr types.float;
      description = ''
        Undocumented
      '';
    };
    instanceInterruptionBehavior = mkOption {
      default = null;
      # example = ;
      type = types.nullOr (types.enum [ "hibernate" "stop" "terminate" ]);
      description = ''
        The behavior when a Spot Instance is interrupted. The default is <code>terminate</code>.
      '';
    };
    instancePoolsToUseCount = mkOption {
      default = null;
      # example = ;
      type = types.nullOr types.int;
      description = ''
        The number of Spot pools across which to allocate your target Spot capacity. Valid only when Spot <b>AllocationStrategy</b> is set to <code>lowest-price</code>. Spot Fleet selects the cheapest Spot pools and evenly allocates your target Spot capacity across the number of Spot pools that you specify.
        Note that Spot Fleet attempts to draw Spot Instances from the number of pools that you specify on a best effort basis. If a pool runs out of Spot capacity before fulfilling your target capacity, Spot Fleet will continue to fulfill your request by drawing from the next cheapest pool. To ensure that your target capacity is met, you might receive Spot Instances from more than the number of pools that you specified. Similarly, if most of the pools have no Spot capacity, you might receive your full target capacity from fewer than the number of pools that you specified.
      '';
    };
    launchSpecifications = mkOption {
      default = [ ];
      example = [
        # Undocumented
      ];
      type = types.nullOr (types.listOf (types.submodule spotFleetLaunchSpecificationOptions));
      description = ''
        The launch specifications for the Spot Fleet request. If you specify <code>LaunchSpecifications</code>, you can't specify <code>LaunchTemplateConfigs</code>. If you include On-Demand capacity in your request, you must use <code>LaunchTemplateConfigs</code>.
      '';
    };
    launchTemplateConfigs = mkOption {
      default = [ ];
      example = [
        # Undocumented
      ];
      type = types.nullOr (types.listOf (types.submodule launchTemplateConfigOptions));
      description = ''
        The launch template and overrides. If you specify <code>LaunchTemplateConfigs</code>, you can't specify <code>LaunchSpecifications</code>. If you include On-Demand capacity in your request, you must use <code>LaunchTemplateConfigs</code>.
      '';
    };
    loadBalancersConfig = mkOption {
      default = null;
      # example = ;
      type = types.nullOr (types.submodule loadBalancersConfigOptions);
      description = ''
        One or more Classic Load Balancers and target groups to attach to the Spot Fleet request. Spot Fleet registers the running Spot Instances with the specified Classic Load Balancers and target groups.
        With Network Load Balancers, Spot Fleet cannot register instances that have the following instance types: C1, CC1, CC2, CG1, CG2, CR1, CS1, G1, G2, HI1, HS1, M1, M2, M3, and T1.
      '';
    };
    onDemandAllocationStrategy = mkOption {
      default = null;
      # example = ;
      type = types.nullOr (types.enum [ "lowestPrice" "prioritized" ]);
      description = ''
        Undocumented
      '';
    };
    onDemandFulfilledCapacity = mkOption {
      default = null;
      # example = ;
      type = types.nullOr types.float;
      description = ''
        Undocumented
      '';
    };
    onDemandMaxTotalPrice = mkOption {
      default = null;
      # example = ;
      type = types.nullOr types.str;
      description = ''
        The maximum amount per hour for On-Demand Instances that you're willing to pay. You can use the <code>onDemandMaxTotalPrice</code> parameter, the <code>spotMaxTotalPrice</code> parameter, or both parameters to ensure that your fleet cost does not exceed your budget. If you set a maximum price per hour for the On-Demand Instances and Spot Instances in your request, Spot Fleet will launch instances until it reaches the maximum amount you're willing to pay. When the maximum amount you're willing to pay is reached, the fleet stops launching instances even if it hasn’t met the target capacity.
      '';
    };
    onDemandTargetCapacity = mkOption {
      default = null;
      # example = ;
      type = types.nullOr types.int;
      description = ''
        The number of On-Demand units to request. You can choose to set the target capacity in terms of instances or a performance characteristic that is important to your application workload, such as vCPUs, memory, or I/O. If the request type is <code>maintain</code>, you can specify a target capacity of 0 and add capacity later.
      '';
    };
    replaceUnhealthyInstances = mkOption {
      default = null;
      # example = ;
      type = types.nullOr types.bool;
      description = ''
        Indicates whether Spot Fleet should replace unhealthy instances.
      '';
    };
    spotMaintenanceStrategies = mkOption {
      default = null;
      # example = ;
      type = types.nullOr (types.submodule spotMaintenanceStrategiesOptions);
      description = ''
        The strategies for managing your Spot Instances that are at an elevated risk of being interrupted.
      '';
    };
    spotMaxTotalPrice = mkOption {
      default = null;
      # example = ;
      type = types.nullOr types.str;
      description = ''
        The maximum amount per hour for Spot Instances that you're willing to pay. You can use the <code>spotdMaxTotalPrice</code> parameter, the <code>onDemandMaxTotalPrice</code> parameter, or both parameters to ensure that your fleet cost does not exceed your budget. If you set a maximum price per hour for the On-Demand Instances and Spot Instances in your request, Spot Fleet will launch instances until it reaches the maximum amount you're willing to pay. When the maximum amount you're willing to pay is reached, the fleet stops launching instances even if it hasn’t met the target capacity.
      '';
    };
    spotPrice = mkOption {
      default = null;
      # example = ;
      type = types.nullOr types.str;
      description = ''
        The maximum price per unit hour that you are willing to pay for a Spot Instance. The default is the On-Demand price.
      '';
    };
    terminateInstancesWithExpiration = mkOption {
      default = null;
      # example = ;
      type = types.nullOr types.bool;
      description = ''
        Indicates whether running Spot Instances are terminated when the Spot Fleet request expires.
      '';
    };
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
    validFrom = mkOption {
      default = null;
      # example = ;
      type = types.nullOr types.str;
      description = ''
        The start date and time of the request, in UTC format (<i>YYYY</i>-<i>MM</i>-<i>DD</i>T<i>HH</i>:<i>MM</i>:<i>SS</i>Z). By default, Amazon EC2 starts fulfilling the request immediately.
      '';
    };
    validUntil = mkOption {
      default = null;
      # example = ;
      type = types.nullOr types.str;
      description = ''
        The end date and time of the request, in UTC format (<i>YYYY</i>-<i>MM</i>-<i>DD</i>T<i>HH</i>:<i>MM</i>:<i>SS</i>Z). After the end date and time, no new Spot Instance requests are placed or able to fulfill the request. If no value is specified, the Spot Fleet request remains until you cancel it.
      '';
    };
  }
  // (import ./common-ec2-options.nix { inherit lib; });

  config =
    mkIf
      # (if cfg.launchSpecifications ?? || cfg then true else throw "\nFailed assertion: ${message}")
      true
      {
        _type = "aws-spot-fleet";
      };

}

