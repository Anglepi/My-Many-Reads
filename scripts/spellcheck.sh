#!/bin/bash
results=./Spellchecker.results
> $results

SpellcheckFile() {
    filename=$1
    extension=${filename##*.}
    if [ $extension == "md" ]; then
        mode=markdown
    else
        mode=tex
    fi

    echo "Spellchecking $1" >> $results
    cat $1 | aspell --lang=en --mode=$mode list | aspell --lang=es --mode=$mode list | sort >> $results
}

foundError=false

for file in $(find ../. -name "*.md" -o -name "*.tex"); do
    linesBeforeCheck=$(cat $results | wc -l)
    SpellcheckFile $file
    linesAfterCheck=$(cat $results | wc -l)
    
    if [ $linesAfterCheck -gt $linesBeforeCheck ]; then
        foundError=true
    else
        echo "No errors found in this file" >> $results
    fi
done

if [ $foundError = true ]; then
    cat $results
    exit 1
else
    printf "Spellcheck complete. No errors found."
    exit 0
fi