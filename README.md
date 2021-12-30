# aws-tools #
Note: these are now dated and may no longer be relevant
### Region Copy for AMIs  ###

<b>regioncp.py</b> - given a CSV file, clone the source AMI from the sourceRegion to regions specified in the CSV file.

     python regioncp.py regions.csv sourceAmi sourceRegion

<b>region.csv</b> - the control file for regioncp.</p>
- <em>Include Region</em> must be 'Y' for the region to be a target of the copy.
- <em>Accounts to Add</em> is for future use.
