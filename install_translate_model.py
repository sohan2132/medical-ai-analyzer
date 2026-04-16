import argostranslate.package
import argostranslate.translate

# Update package index
argostranslate.package.update_package_index()

# Get available packages
available_packages = argostranslate.package.get_available_packages()

# Find Thai → English package
package_to_install = next(
    filter(lambda x: x.from_code == "th" and x.to_code == "en", available_packages)
)

# Download and install
argostranslate.package.install_from_path(package_to_install.download())

print("Thai → English translation model installed successfully.")