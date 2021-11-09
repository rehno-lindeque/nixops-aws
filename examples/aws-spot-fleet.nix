{ region ? "us-east-1"
, accessKeyId ? "testing"
, ...
}:
{
  network.description = "AWS Spot Fleet testing";
  resources.awsSpotFleetRequest = {
    inherit region accessKeyId;
    iamFleetRole = "arn:aws:iam::00000000:role/spot-fleet";
    # spotPrice = 1;
    allocationStrategy = "diversified";
    targetCapacity = 2;
    # validUntil = 
    # launchSpecifications = [{
    #   # instanceType = "m4.....";
    #   # ami = "ami-00000000";
    #   # keyName = "key";
    #   # spot_price = "";
    #   # placementTenancy = "";
    #   # iamInstanceProfileArn = "";
    # }];

    # tags = 
  };
}
