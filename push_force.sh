#!/bin/bash

echo "Напиши комент, нажми [ENTER]:"

read comment

git add .
git commit -a -m "$comment" --amend
git push -u origin master --force
