class Easyedatool < Formula
  desc "Offline CLI for EasyEDA Pro board projects"
  homepage "https://github.com/cc38324/PcbCliTool"
  version "0.2.7"
  license :cannot_represent

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/cc38324/PcbCliTool/releases/download/v0.2.7/easyedatool-0.2.7-macos-arm64.tar.gz"
      sha256 "17877ab611d737243ca4864cbe8f07d22c13fa29dd81f882bf84ab711a80ab7b"
    end
  end

  def install
    bin.install "easyedatool"
  end

  test do
    assert_match "0.2.7", shell_output("#{bin}/easyedatool --version")
  end
end
