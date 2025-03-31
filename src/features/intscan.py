import subprocess

class IntegrityCheckManager:
    def run_sfc(self):
        "Runs sfc command"
        print("Running System File Checker...")
        try:
            result = subprocess.run(["sfc", "/scannow"], capture_output=True, text=True)
            print(result.stdout) #Prints output
            if result.returncode == 0:
                print("System File Checker was completed successfully.")
            else:
                print("System File Checker encountered issues.")
        except Exception as e:
            print(f"The process encountered issues: {str(e)}.")

    def run_dism(self):
        print("Running DISM")
        try:
            result = subprocess.run(["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"], capture_output=True, text=True)
            print(result.stdout)
            if result.returncode == 0:
                print("DISM completed successfully.")
            else:
                print("DISM encountered issues")
        except Exception as e:
            print(f"The process was not completed: {str(e)}")

    def run_integrity_check(self):
        """Run both"""
        self.run_sfc()
        self.run_dism()