class Easyedatool < Formula
  desc "Offline CLI for EasyEDA Pro board projects"
  homepage "https://github.com/cc38324/PcbCliTool"
  version "0.3.0"
  license :cannot_represent

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/cc38324/PcbCliTool/releases/download/v0.3.0/easyedatool-0.3.0-macos-arm64.tar.gz"
      sha256 "5ba70dfee3d324e46245e03a4ff8f42d24eccf8ebcddd13d7997d4ff62e51a93"
    end
  end

  def install
    libexec.install "easyedatool", "VERSION", "runtime"
    bin.write_exec_script libexec/"easyedatool"
  end

  test do
    assert_match "0.3.0", shell_output("#{bin}/easyedatool --version")
  end
end
