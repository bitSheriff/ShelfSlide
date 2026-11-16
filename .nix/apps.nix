{ pkgs, pythonEnv, src }:

{
  tests = {
    type = "app";
    program = "${pkgs.writeShellApplication {
      name = "shelfslide-tests";
      runtimeInputs = [ pythonEnv ];
      text = ''
        cd ${src}
        python -m pytest -p no:cacheprovider "$@"
      '';
    }}/bin/shelfslide-tests";
  };
}
