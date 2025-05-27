# Generates SVG files from D2 files in the current directory
for file in *.d2; do
  d2 "$file" "${file%}.svg" -p 4002 &
done