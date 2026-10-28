class Easyedatool < Formula
  desc "Offline CLI for EasyEDA Pro board projects"
  homepage "https://github.com/cc38324/PcbCliTool"
  version "0.2.3"
  license :cannot_represent

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/cc38324/PcbCliTool/releases/download/v0.2.3/easyedatool-0.2.3-macos-arm64.tar.gz"
      sha256 "9217316e6302fca7d74a5b22e206e90e1579904dbb5e0aed668ab267131beeeb"
    end
  end

  def install
    bin.install "easyedatool"
  end

  test do
    assert_match "0.2.3", shell_output("#{bin}/easyedatool --version")
  end
end
