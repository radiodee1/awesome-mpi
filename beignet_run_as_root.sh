echo 0 > /sys/module/i915/parameters/enable_cmd_parser 

# As of 9/2/2014 this is needed to allow Beignet to work.
# It's not needed otherwise.
#
# Remains in effect until system restart.
