"""
Example Ganga script for running an executable with varying arguments.

This example uses generic Ganga functionality.  It doesn't contain
anything specific to working with Scikit-rt.
"""
import platform

# Define an Executable application, for running a user-written script.
app = Executable()
app.exe = File("echo.sh")
# Don't define arguments here, as they will be passed via the splitter.
app.args = []
# Optionally define environment variables.
app.env = {}

# Define argument to be passed to the script in different subjobs.
splitter = ArgSplitter()
# Each list item is a list of arguments to pass (here only a single argument).
splitter.args = [["Hello!"], ["Goodbye!"]]

# Define processing system.
if "Linux" == platform.system():
    backend = Condor()
    backend.cdf_options["request_memory"]="1G"
else:
    backend = Local()

# Define merging of subjob outputs
merger = SmartMerger()
merger.files = ["stderr", "stdout"]
merger.ignorefailed = True
postprocessors = [merger]

# Define job name
name = "echo"

# Create the job, and submit to processing system
j = Job(application=app, backend=backend, splitter=splitter,
        postprocessors=postprocessors, name=name)
j.submit()
