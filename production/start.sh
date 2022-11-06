  
#!/usr/bin/env bash

cd "$(dirname "$0")"
waitress-serve predict:app
