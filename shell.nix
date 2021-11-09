{ pkgs ? import <nixpkgs> {} }:
let
  overrides = import ./overrides.nix { inherit pkgs; };
in pkgs.mkShell {
  buildInputs = [
    (pkgs.poetry2nix.mkPoetryEnv {
      projectDir = ./.;
      overrides = pkgs.poetry2nix.overrides.withDefaults overrides;
      python = pkgs.python39;
    })
    pkgs.poetry
    pkgs.nixpkgs-fmt
  ];
}
