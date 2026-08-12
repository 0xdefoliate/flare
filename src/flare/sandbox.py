SEATBELT_PROFILE = """
(version 1)
(deny default)

(allow file-read*
    (subpath "/System")
    (subpath "/Library")
    (subpath "/usr/lib")
    (literal "/bin/realpath")
    (literal "/usr/bin/env")
    (literal (param "ENTRYPOINT"))
    (literal "/")
)

(allow process-fork)
(allow process-exec)
""".strip()