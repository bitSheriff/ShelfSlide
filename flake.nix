{
  description = "ShelfSlide dev environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in
    {
      devShells = forAllSystems (system:
        let pkgs = nixpkgs.legacyPackages.${system};
        in {
          default = pkgs.mkShell {
            packages = with pkgs; [
              uv
              python312
              openjpeg # libopenjp2, required by Pillow's JPEG2000 codec
            ];

            # keep uv's managed interpreter/venv local to the repo
            UV_PYTHON_PREFERENCE = "managed";

            shellHook = ''
              echo "ShelfSlide devShell: run 'uv sync' then 'uv run shelfslide.py'"
            '';
          };
        });
    };
}
