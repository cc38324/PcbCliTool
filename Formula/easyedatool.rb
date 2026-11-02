class Easyedatool < Formula
  desc "Offline CLI for EasyEDA Pro board projects"
  homepage "https://github.com/cc38324/PcbCliTool"
  version "0.2.6"
  license :cannot_represent

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/cc38324/PcbCliTool/releases/download/v0.2.6/easyedatool-0.2.6-macos-arm64.tar.gz"
      sha256 "6802ef232687444a423779453503eb68dab838cf446585c118a39ed372a65a4e"
    end
  end

  def install
    bin.install "easyedatool"
  end

  test do
    assert_match "0.2.6", shell_output("#{bin}/easyedatool --version")
  end
end
