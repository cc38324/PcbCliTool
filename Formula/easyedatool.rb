class Easyedatool < Formula
  desc "Offline CLI for EasyEDA Pro board projects"
  homepage "https://github.com/cc38324/PcbCliTool"
  version "0.2.1"
  license :cannot_represent

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/cc38324/PcbCliTool/releases/download/v0.2.1/easyedatool-0.2.1-macos-arm64.tar.gz"
      sha256 "7f71986ee5f3db4facaa36ab90837aa384fc66ad637e544ff704aa68acb37274"
    end
  end

  def install
    bin.install "easyedatool"
  end

  test do
    assert_match "0.2.1", shell_output("#{bin}/easyedatool --version")
  end
end
