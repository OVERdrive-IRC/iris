from __future__ import print_function
import sys
import subprocess


def fail(*message):
    print("\n".join(message), file=sys.stderr)
    sys.exit(1)


def warn(*message):
    print("warning:", "\nwarning: ".join(message), "\n", file=sys.stderr)


def check_dependencies():
    i = 0
    check_twisted()
    check_win32()
    i += check_java()
    i += check_git()

    print("0 errors, %d warnings." % i)

    if i == 0:
        print("looks like you've got everything you need to run qwebirc!")
    else:
        print("you can run qwebirc despite these.")

    f = open(".checked", "w")
    f.close()


def check_win32():
    if not sys.platform.startswith("win"):
        return

    try:
        import win32con
    except ImportError:
        fail("qwebirc requires pywin32, see:",
             "http://sourceforge.net/project/showfiles.php?group_id=78018")


def check_java():
    def java_warn(specific):
        warn(specific, "java is not required, but allows qwebirc to compress output,",
             "making it faster to download.", "you can get java at http://www.java.com/")

    try:
        p = subprocess.Popen(
            ["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()
        if p.wait() != 0:
            java_warn("something went wrong looking for java.")
        return 1
    except:  # ugh
        java_warn("couldn't find java.")
        return 1

    return 0


def check_git():
    def git_warn(specific):
        warn(specific, "git is not required, but allows qwebirc to save bandwidth by versioning.",
             "you can get git at http://git-scm.com/")

    try:
        p = subprocess.Popen(["git", "show", "--pretty=oneline",
                              "--quiet"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()
        status = p.wait()
        if status != 0 and status != 1:
            git_warn("something went wrong looking for git.")
            return 1
    except:  # ugh
        git_warn("couldn't find git.")
        return 1
    return 0


def check_twisted():
    try:
        import twisted
    except ImportError:
        fail(
            "qwebirc requires twisted (at least 8.2.0), see http://twistedmatrix.com/")

    def twisted_fail(x, y=None):
        fail("you don't seem to have twisted's %s module." % x,
             "your distro is most likely modular, look for a twisted %s package%s." % (x, " %s" % y if y else "",))

    try:
        import twisted.names
    except ImportError:
        twisted_fail("names")

    try:
        import twisted.mail
    except ImportError:
        twisted_fail("mail")

    try:
        import twisted.web
    except ImportError:
        twisted_fail("web", "(not web2)")

    try:
        import twisted.words
    except ImportError:
        twisted_fail("words")

def has_checked():
    try:
        f = open(".checked", "r")
        f.close()
        return True
    except:
        pass

    try:
        f = open(os.path.join("bin", ".checked"), "r")
        f.close()
        return True
    except:
        pass

    return False


def vcheck():
    if not has_checked():
        sys.stderr.write("first run, checking dependencies...\n")
        sys.stderr.flush()
        check_dependencies()

if __name__ == "__main__":
    check_dependencies()
