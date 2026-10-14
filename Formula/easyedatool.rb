class Easyedatool < Formula
  desc "Offline CLI for EasyEDA Pro board projects"
  homepage "https://github.com/cc38324/PcbCliTool"
  version "0.2.0"
  license :cannot_represent

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/cc38324/PcbCliTool/releases/download/v0.2.0/easyedatool-0.2.0-macos-arm64.tar.gz"
      sha256 "70f2eff5ff7128aacb2eee2653167b967632004df2680625ce76d1449b475e38"
    end
  end

  def install
    bin.install "easyedatool"
  end

  test do
    assert_match "0.2.0", shell_output("#{bin}/easyedatool --version")
  end
end
