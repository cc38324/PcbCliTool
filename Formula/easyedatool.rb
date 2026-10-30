class Easyedatool < Formula
  desc "Offline CLI for EasyEDA Pro board projects"
  homepage "https://github.com/cc38324/PcbCliTool"
  version "0.2.5"
  license :cannot_represent

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/cc38324/PcbCliTool/releases/download/v0.2.5/easyedatool-0.2.5-macos-arm64.tar.gz"
      sha256 "6df45169e701d6d46c9289590cf00004de655923ab655285095778e18e1f78cb"
    end
  end

  def install
    bin.install "easyedatool"
  end

  test do
    assert_match "0.2.5", shell_output("#{bin}/easyedatool --version")
  end
end
