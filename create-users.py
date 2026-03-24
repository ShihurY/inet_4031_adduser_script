#!/usr/bin/python3

# INET4031
# Shihur Yang
# 3/23/26
# 3/23/26

# os is used so the script can run system commands like adduser and passwd
# re is used to check patterns in the input such as lines starting with #
# sys is used to read each line coming into the script
import os
import re
import sys

def main():
    for line in sys.stdin:

        # check if the line starts with # which means it is just a comment
        # these lines should be ignored and not used for creating users
        match = re.match("^#", line)

        # clean up the line and split it using :
        # this separates the input into pieces like username password and groups
        fields = line.strip().split(':')

        # skip anything that is a comment or not formatted with exactly 5 parts
        # this prevents bad or incomplete data from being used
        if match or len(fields) != 5:
            continue

        # assign values from the list to variables
        # gecos builds the full name field using first and last name
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])

        # split the groups in case multiple are listed with commas
        groups = fields[4].split(',')

        # show which user is being processed
        print("==> Creating account for %s..." % (username))

        # create the command that adds the user without setting a password yet
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)

        # print it first to check then run it when ready
        # print(cmd)
        # os.system(cmd)

        # move on to setting the password
        print("==> Setting the password for %s..." % (username))

        # send the password into passwd twice so it sets automatically
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)

        # same idea print first then run
        # print(cmd)
        # os.system(cmd)

        for group in groups:
            # if the group is - it means no group should be added
            # otherwise add the user to each group listed
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                # print(cmd)
                # os.system(cmd)

if __name__ == '__main__':
    main()
