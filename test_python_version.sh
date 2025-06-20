PYTHON_VERSION=$(python --version 2>&1 | cut -d ' ' -f 2)
MAJOR_PYTHON_VERSION=$(echo "$PYTHON_VERSION" | cut -d '.' -f 1)
PYTHON_311_VERSION=$(/usr/bin/python --version 2>&1 | cut -d '.' -f 2)

if [ -L /usr/bin/python ]; then
        if (( "MAJOR_PYTHON_VERSION" != 3 )) ||  (( "PYTHON_311_VERSION" <= 10 )) ; then
                echo 'Incorrect Python Version'
                exit 1
        else
              echo 'good'
        fi
else
  echo "my_symlink is NOT a symbolic link."
  exit 1
fi