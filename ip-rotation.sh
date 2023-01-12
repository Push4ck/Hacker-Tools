#!/bin/bash

# Set the list of IP addresses to rotate through
ips=("123.456.789.0" "123.456.789.1" "123.456.789.2")

# Set the URL to request
url="http://example.com"

# Loop through the list of IPs
for ip in "${ips[@]}"; do
  # Make a request using the current IP address
  curl --interface $ip $url
done
