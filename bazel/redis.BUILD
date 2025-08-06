########################################
# redis/BUILD.bazel – use system-installed redis
########################################

# Only the Windows binaries are real source files in the archive.
exports_files(
    [
        "redis-server.exe",
        "redis-cli.exe",
    ],
    visibility = ["//visibility:public"],
)

# Linux / macOS: copy the redis binaries already on the host into Bazel’s
# output tree.  Tagged "local" so it never runs on a remote worker that might
# not have Redis installed.
genrule(
    name = "bin",
    srcs = [],
    outs = [
        "redis-server",
        "redis-cli",
    ],
    cmd = select({
        "@platforms//os:osx": """
            set -euo pipefail
            SRV=$$(command -v redis-server)
            CLI=$$(command -v redis-cli)
            [ -x "$$SRV" ] || { echo "redis-server not found on PATH"; exit 1; }
            [ -x "$$CLI" ] || { echo "redis-cli not found on PATH";   exit 1; }
            cp "$$SRV" "$(location redis-server)"
            cp "$$CLI" "$(location redis-cli)"
            chmod +x "$(location redis-server)" "$(location redis-cli)"
        """,
        # Default covers Linux and any other non-macOS Unix-like host.
        "//conditions:default": """
            set -euo pipefail
            SRV=$$(command -v redis-server)
            CLI=$$(command -v redis-cli)
            [ -x "$$SRV" ] || { echo "redis-server not found on PATH"; exit 1; }
            [ -x "$$CLI" ] || { echo "redis-cli not found on PATH";   exit 1; }
            cp "$$SRV" "$(location redis-server)"
            cp "$$CLI" "$(location redis-cli)"
            chmod +x "$(location redis-server)" "$(location redis-cli)"
        """,
    }),
    visibility = ["//visibility:public"],
    tags = ["local"],
)


