class Easyedatool < Formula
  desc "Offline CLI for EasyEDA Pro board projects"
  homepage "https://github.com/cc38324/PcbCliTool"
  version "0.2.4"
  license :cannot_represent

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/cc38324/PcbCliTool/releases/download/v0.2.4/easyedatool-0.2.4-macos-arm64.tar.gz"
      sha256 "9e9177179ec1f51ad5c8216337e19c33efb76e823aa7606989548c0a3bf75482"
    end
  end

  def install
    bin.install "easyedatool"
  end

  test do
    assert_match "0.2.4", shell_output("#{bin}/easyedatool --version")
  end
end
