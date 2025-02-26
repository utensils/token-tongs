{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    requests
    pytest
    pytest-cov
    rumps
    pip
  ]);
in
pkgs.mkShell {
  buildInputs = [
    pythonEnv
  ];

  shellHook = ''
    # Create and activate a virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
      ${pythonEnv}/bin/python -m venv venv
    fi
    source venv/bin/activate

    # Install additional requirements
    pip install requests-mock
  '';
}