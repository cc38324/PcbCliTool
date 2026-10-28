class Easyedatool < Formula
  desc "Offline CLI for EasyEDA Pro board projects"
  homepage "https://github.com/cc38324/PcbCliTool"
  version "0.2.2"
  license :cannot_represent

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/cc38324/PcbCliTool/releases/download/v0.2.2/easyedatool-0.2.2-macos-arm64.tar.gz"
      sha256 "7fa083fb085f02fc00d57e19ae5a2b9bfafee21747c0263437e04f63171609ed"
    end
  end

  def install
    bin.install "easyedatool"
  end

  test do
    assert_match "0.2.2", shell_output("#{bin}/easyedatool --version")
  end
end
