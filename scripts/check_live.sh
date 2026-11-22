#!/usr/bin/env bash
set -Eeuo pipefail
BASE="${1:-https://vitoog.github.io/Landingpage}"; BASE="${BASE%/}"
for path in / /ru/ /services/ /ru/services/ /robots.txt /sitemap.xml; do
 echo "== $BASE$path"
 curl --fail --location --silent --show-error --max-time 25 "$BASE$path" -o /dev/null
done
echo "PASS: all configured live routes returned HTTP success."
