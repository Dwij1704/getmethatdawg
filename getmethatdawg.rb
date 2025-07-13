class Yoo < Formula
  desc "Zero-config deploy & MCP for Python agents"
  homepage "https://github.com/yoo-deploy/yoo"
  url "https://github.com/yoo-deploy/yoo/archive/v0.1.0.tar.gz"
  sha256 "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"  # This needs to be updated with actual hash
  license "MIT"

  depends_on "python@3.11"
  depends_on "docker"
  depends_on "flyctl"

  def install
    # Install the main yoo command
    bin.install "bin/yoo"
    bin.install "bin/yoo-builder"
    
    # Install the Python CLI orchestrator
    libexec.install "libexec/yoo-cli.py"
    
    # Install the yoo-sdk Python package
    cd "yoo-sdk" do
      system Formula["python@3.11"].opt_bin/"python3", "-m", "pip", "install", 
             "--target=#{libexec}", "."
    end
    
    # Create share directory for templates and resources
    (share/"yoo").mkpath
    
    # Note: Templates would be installed here in a real deployment
    # For now, they're embedded in the builder code
  end

  test do
    # Test that the command exists and shows help
    assert_match "yoo - Zero-config deploy for Python agents", shell_output("#{bin}/yoo --help")
    
    # Test that dependencies are mentioned if not available
    # This will fail if docker/flyctl aren't installed, which is expected
  end
end 