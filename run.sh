#!/bin/bash
VIRT_ENV="bin"
check_requirements(){
  rc=0
  echo "Checking neccesary constraints to run the project"
  echo -ne "1. requirements.txt exists\t"
  if [[ -r "requirements.txt" ]] ; then echo "OK" ; else echo "NO" ; rc=1; fi

  echo -ne "2. virtual env exists\t"
  if [[ -r "$VIRT_ENV/bin/activate" ]] ; then echo "OK" ; else echo "NO, setting up" ; python -m venv "$VIRT_ENV" ; fi

  echo -ne "3. .env exists\t"
  if [[ -r ".env" ]] ; then echo "OK" ; else echo "NO, kindly refer .env.demo" ; rc=1 ; fi

  return "$rc"
}
if check_requirements ; then echo "All requirements satisfied" ; else echo "Requirements not satisfied" ; exit 1 ; fi
echo "Using virtual env located at $VIRT_ENV"
if ! source "$VIRT_ENV/bin/activate" ; then echo "Error Occurred" ; exit 1 ; fi
echo "Installing all requirements"
if ! pip install -qr requirements.txt  ; then echo "Error Occurred" ; exit 1 ; fi
echo "Running flask server"
if ! flask run ; then echo "Error Occurred" ; exit 1; fi
