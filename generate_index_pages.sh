#!/bin/bash

TEMPLATES_DIR="templates"
OUTPUT_FILE="$TEMPLATES_DIR/index.html"

echo "Generating index at $OUTPUT_FILE..."

# Start writing HTML
cat > "$OUTPUT_FILE" <<EOF
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Captive Portal Template Index</title>
</head>
<body>
  <h1>Captive Portal Templates</h1>
EOF

# Find and group HTML files
prev_theme=""
prev_class=""

while IFS= read -r file_path; do
  # Remove templates/ prefix
  relative_path="${file_path#$TEMPLATES_DIR/}"

  # Split path into components
  theme=$(echo "$relative_path" | cut -d'/' -f1)
  class=$(echo "$relative_path" | cut -d'/' -f2)
  file=$(basename "$relative_path")

  # If new group, print header
  if [[ "$theme" != "$prev_theme" || "$class" != "$prev_class" ]]; then
    # Close previous list
    if [[ "$prev_theme" != "" ]]; then
      echo "</ul><br>" >> "$OUTPUT_FILE"
    fi
    echo "<h2>$theme / $class</h2>" >> "$OUTPUT_FILE"
    echo "<ul>" >> "$OUTPUT_FILE"
    prev_theme="$theme"
    prev_class="$class"
  fi

  # Add file link
  echo "  <li><a href=\"$relative_path\">$file</a></li>" >> "$OUTPUT_FILE"

done < <(find "$TEMPLATES_DIR" -type f -name "*.html" ! -name "index.html" | sort)

# Close last group
if [[ "$prev_theme" != "" ]]; then
  echo "</ul><br>" >> "$OUTPUT_FILE"
fi

# Finish HTML
cat >> "$OUTPUT_FILE" <<EOF
</body>
</html>
EOF

echo "✅ index.html generated at $OUTPUT_FILE"
