class Easyedatool < Formula
  desc "Offline CLI for EasyEDA Pro board projects"
  homepage "https://github.com/cc38324/PcbCliTool"
  version "0.3.1"
  license :cannot_represent

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/cc38324/PcbCliTool/releases/download/v0.3.1/easyedatool-0.3.1-macos-arm64.tar.gz"
      sha256 "3c15fd7a1d29957964152c3bad8102ee58582931d9a5e8bce4653d963b8719d1"
    end
  end

  def install
    libexec.install "easyedatool", "VERSION", "runtime"
    bin.write_exec_script libexec/"easyedatool"
  end

  test do
    assert_match "0.3.1", shell_output("#{bin}/easyedatool --version")
  end
end
