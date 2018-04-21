
import csv
import sys

import boto3


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
        readCSV = csv.reader(csvfile) # don't need any qualifiers, use defaults
        for row in readCSV:
            if row[0] != "Name" and row[2] is "Y":
                # put some error logic here (try block for region lines being undersized)
                # use the 'strict=true' logic on the reader to raise Error exception
                regions[row[1]] = row[3]
    return


def clone_ami_into_regions(ami_id, source_region, dest_regions):
    """
    A method that clones the AMI into regions specified.

    :param ami_id: the id of the base AMI
    :param source_region: the region the base AMI is located in
    :param dest_regions: a list of region ids to clone the ami into

    :return:a list of ami id, which corresponds to the list of regions.
    """
    new_ami_ids = {}

    if len(dest_regions) > 0:
        ec2 = boto3.resource('ec2', region_name=source_region)
        # get a reference to the base ami that will be copied FROM
        image = ec2.Image(ami_id)
        print("Image %s: " % image)
        for r in dest_regions:
            ec2_region = boto3.client('ec2', region_name=r)
            result = ec2_region.copy_image(SourceImageId=ami_id,
                                           Name=image.name,
                                           Description=image.description,
                                           SourceRegion=source_region,
                                           DryRun=False
                                           )
            new_ami_ids[r] = result['ImageId']

    return new_ami_ids



if __name__ == '__main__':  # pragma: no cover
    params = ""
    if len(sys.argv) > 1:
        csv_filename = sys.argv[1]
    else:
        print("No parameter (.csv) file provided.")
        sys.exit(1)

    cli_data = []
    if len(sys.argv) > 2:
        cli_data = sys.argv[2:]

    print("Processing %s as regions file" % csv_filename)
    print("Using cli data: %s" % cli_data)

    # command line:  python regioncp regions.csv sourceAmi sourceRegion
    my_regions = {}
    source_ami = cli_data[0]
    source_region = cli_data[1]

    get_regions_accounts(csv_filename, my_regions)
    print ("retrieved regions: ", my_regions)

    new_ami_list = clone_ami_into_regions(source_ami, source_region, my_regions)

    print ("returned AMI list: ", new_ami_list)

