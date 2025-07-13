class GetmethatdawgLocal < Formula
  desc "Zero-config deployment for Python AI agents and web services"
  homepage "https://github.com/yourusername/getmethatdawg"
  # For local testing, we'll use the current directory
  url "file://#{Dir.pwd}"
  version "0.1.0"
  license "MIT"

  depends_on "python@3.11"
  # Skip docker and flyctl for local testing to avoid dependency issues

  def install
    # Install Python dependencies  
    system "python3.11", "-m", "pip", "install", "--target", "#{libexec}/lib/python", "flask>=2.0.0", "gunicorn>=20.0.0"
    
    # Copy getmethatdawg package directly
    (libexec/"lib/python").mkpath
    cp_r "getmethatdawg-sdk/getmethatdawg", "#{libexec}/lib/python/"
    
    # Create the main getmethatdawg executable
    (bin/"getmethatdawg").write <<~EOS
      #!/bin/bash
      
      # getmethatdawg - Zero-config deploy for Python agents
      # Homebrew installation version
      
      set -euo pipefail
      
      # Set up Python path to find getmethatdawg modules
      export PYTHONPATH="#{libexec}/lib/python:$PYTHONPATH"
      export GETMETHATDAWG_HOME="#{libexec}"
      export GETMETHATDAWG_LIBEXEC="#{libexec}/libexec"
      
      # Show version
      show_version() {
          echo "getmethatdawg version #{version}"
          echo "Zero-config deploy for Python agents"
          echo "Installed via Homebrew (local test)"
      }
      
      # Show usage
      show_usage() {
          cat << EOF
      getmethatdawg - Zero-config deploy for Python agents
      
      Usage:
          getmethatdawg --help                            Show this help message
          getmethatdawg --version                         Show version information
      
      This is a local test installation.
      For full functionality, install Docker and flyctl.
      
      EOF
      }
      
      # Main function
      main() {
          case "${1:-}" in
              --help|-h)
                  show_usage
                  ;;
              --version|-v)
                  show_version
                  ;;
              "")
                  echo "getmethatdawg local test installation working!"
                  show_usage
                  ;;
              *)
                  echo "This is a local test version. Command '$1' not implemented."
                  show_usage
                  ;;
          esac
      }
      
      # Run main function with all arguments
      main "$@"
    EOS
    
    # Install completions for bash and zsh
    bash_completion.install "scripts/completions/getmethatdawg.bash" => "getmethatdawg"
    zsh_completion.install "scripts/completions/_getmethatdawg"
  end

  def caveats
    <<~EOS
      getmethatdawg (LOCAL TEST) has been installed! 🚀
      
      This is a local test installation to verify the homebrew formula works.
      
      Test with: getmethatdawg --version
      
      For full functionality, you'll need:
        - Docker (for building)
        - flyctl (for deployment)
      
    EOS
  end

  test do
    # Test that the getmethatdawg command works
    assert_match "getmethatdawg version", shell_output("#{bin}/getmethatdawg --version")
  end
end 