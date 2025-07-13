class getmethatdawg < Formula
  desc "Zero-config deploy & MCP for Python agents"
  homepage "https://github.com/Dwij1704/getmethatdawg"
  url "https://github.com/Dwij1704/getmethatdawg/archive/v0.0.4.tar.gz"
  sha256 "cb8c2883119182140084ed294996b24608c95e5dd798e9db7e98b63d0835a730"
  license "MIT"

  depends_on "python@3.11"
  depends_on "docker"
  depends_on "flyctl"

  def install
    # Install the main getmethatdawg command
    bin.install "bin/getmethatdawg"
    bin.install "bin/getmethatdawg-builder"
    
    # Install the Python CLI orchestrator
    libexec.install "libexec/getmethatdawg-cli.py"
    
    # Install the getmethatdawg-sdk Python package
    cd "getmethatdawg-sdk" do
      system Formula["python@3.11"].opt_bin/"python3", "-m", "pip", "install", 
             "--target=#{libexec}", "."
    end
    
    # Create share directory for templates and resources
    (share/"getmethatdawg").mkpath
    
    # Note: Templates would be installed here in a real deployment
    # For now, they're embedded in the builder code
  end

  test do
    # Test that the command exists and shows help
    assert_match "getmethatdawg - Zero-config deploy for Python agents", shell_output("#{bin}/getmethatdawg --help")
    
    # Test that dependencies are mentioned if not available
    # This will fail if docker/flyctl aren't installed, which is expected
  end
end 