scripts_folder="scripts/"
tests_folder="tests/"
echo "linting the following folders:
- "$scripts_folder"
- "$tests_folder""
pylint "$scripts_folder" "$tests_folder"