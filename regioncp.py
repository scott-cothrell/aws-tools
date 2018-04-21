
import csv
import sys

import boto3

BOTO3_EC2 = "ec2"


def get_regions_accounts(filename, regions):
    """
    A method that fills in the list of regions[] and any included accounts per region
    by reading from a CSV filename passed in as a parameter.
    For a given entry, it may be a region with no accounts or a region with accounts.

    :param filename: name of comma separated values (CSV) file that contains the region and account data.
    :param regions: dictionary built with the selected regions as index.

    :return: dict with accounts by region.
    """

    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[0] != "Name" and row[2] is "Y":
                # put some error logic here (try block for region lines being undersized)
                regions[row[1]] = row[3]
    return


def clone_ami_into_regions(ami_id, base_region, regions, access_key_id, secret_access_key):
    """
    A method that clones the AMI into regions specified.

    :param ami_id: the id of the base AMI
    :param base_region: the region the base AMI is located in
    :param regions: a list of region ids to clone the ami into
    :param access_key_id: the access id for the aws account
    :param secret_access_key: the secret access key for the aws account

    :return:a list of ami id, which corresponds to the list of regions.
    """

    ami_ids = {}

    if len(regions) > 0:
        ec2 = boto3.resource(BOTO3_EC2,
                             aws_access_key_id=access_key_id,
                             aws_secret_access_key=secret_access_key,
                             region_name=base_region)
        # get a reference to the base ami that will be copied FROM
        image = ec2.Image(ami_id)
        print("Image %s: " % image)
        for r in regions:
            ec2_region = boto3.client(BOTO3_EC2,
                                      aws_access_key_id=access_key_id,
                                      aws_secret_access_key=secret_access_key,
                                      region_name=r)
            result = ec2_region.copy_image(SourceImageId=ami_id,
                                           Name=image.name,
                                           Description=image.description,
                                           SourceRegion=base_region)
            ami_ids[r] = result['ImageId']

    return ami_ids





if __name__ == '__main__':  # pragma: no cover
    params = ""
    if len(sys.argv) > 1:
        params = sys.argv[1]
    else:
        print("No parameter (.csv) file provided.")
        sys.exit(1)

    cli = []
    if len(sys.argv) > 2:
        cli = sys.argv[2:]

    print("Processing %s as regions file" % params)
    print("Using cli: %s" % cli)

    # command line:  python regioncp regions.csv sourceAmi sourceRegion accessKey secretAccessKey
    my_regions = {}
    source_ami = cli[0]
    source_region = cli[1]
    my_access_key = cli[2]
    my_secret_key = cli[3]

    get_regions_accounts(params, my_regions)
    print ("retrieved regions: ", my_regions)

#    new_ami_list = clone_ami_into_regions(source_ami, source_region, my_regions, my_access_key, my_secret_key)
#    new_ami_list = {'us-east-1': 'ami-a58ddadf', 'us-west-2': 'ami-a746eddf'}
#    print ("returned AMI list ", new_ami_list)

#    add_account_to_ami(my_regions, new_ami_list, my_access_key, my_secret_key)
