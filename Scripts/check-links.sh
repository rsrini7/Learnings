#!/bin/bash
# Link Checker for Markdown Files
# Usage: ./check-links.sh [directory]

DIR="${1:-.}"
BROKEN=0
TOTAL=0

echo "🔍 Scanning markdown files in: $DIR"
echo "=================================="

find "$DIR" -name "*.md" -type f | sort | while read -r mdfile; do
    dir=$(dirname "$mdfile")
    file_broken=0
    
    # Extract image refs: ![...](path)
    while IFS= read -r match; do
        # Extract path from match
        path=$(echo "$match" | sed -E 's/.*\]\(([^)]+)\)/\1/')
        
        # Skip URLs
        [[ "$path" =~ ^https?:// ]] && continue
        [[ "$path" =~ ^mailto: ]] && continue
        
        # Remove anchors
        path="${path%%#*}"
        [[ -z "$path" ]] && continue
        
        # Handle angle brackets: <path>
        path="${path#<}"
        path="${path%>}"
        
        # Resolve relative path
        if [[ "$path" == /* ]]; then
            fullpath="${DIR}${path}"
        else
            fullpath="${dir}/${path}"
        fi
        
        # Normalize path
        fullpath=$(realpath -m "$fullpath" 2>/dev/null || echo "$fullpath")
        
        TOTAL=$((TOTAL + 1))
        
        if [[ ! -e "$fullpath" ]]; then
            if [[ $file_broken -eq 0 ]]; then
                echo ""
                echo "📄 $mdfile"
                file_broken=1
            fi
            echo "  ❌ BROKEN: $path"
            echo "     Expected: $fullpath"
            BROKEN=$((BROKEN + 1))
        fi
    done < <(grep -o '!\[[^]]*\]([^)]*)' "$mdfile" 2>/dev/null)
    
    # Extract file links: [...](path) (not images)
    while IFS= read -r match; do
        path=$(echo "$match" | sed -E 's/.*\]\(([^)]+)\)/\1/')
        
        [[ "$path" =~ ^https?:// ]] && continue
        [[ "$path" =~ ^mailto: ]] && continue
        [[ "$path" =~ ^# ]] && continue
        
        path="${path%%#*}"
        [[ -z "$path" ]] && continue
        
        path="${path#<}"
        path="${path%>}"
        
        if [[ "$path" == /* ]]; then
            fullpath="${DIR}${path}"
        else
            fullpath="${dir}/${path}"
        fi
        
        fullpath=$(realpath -m "$fullpath" 2>/dev/null || echo "$fullpath")
        
        TOTAL=$((TOTAL + 1))
        
        if [[ ! -e "$fullpath" ]]; then
            if [[ $file_broken -eq 0 ]]; then
                echo ""
                echo "📄 $mdfile"
                file_broken=1
            fi
            echo "  ❌ BROKEN: $path"
            echo "     Expected: $fullpath"
            BROKEN=$((BROKEN + 1))
        fi
    done < <(grep -o '\[[^]]*\]([^)]*)' "$mdfile" 2>/dev/null | grep -v '^\!')
done

echo ""
echo "=================================="
echo "📊 Summary"
echo "   Total links checked: $TOTAL"
echo "   Broken links found:  $BROKEN"

if [[ $BROKEN -eq 0 ]]; then
    echo "   ✅ All links valid!"
else
    echo "   ⚠️  Some links need fixing"
fi
