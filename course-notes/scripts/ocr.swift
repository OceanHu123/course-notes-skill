// OCR a single image with the macOS Vision framework.
// usage: ocr <image-path>
// Compiled on demand by scripts/ocr_pages.py; no external install required.

import Foundation
import Vision
import AppKit

let args = CommandLine.arguments
guard args.count >= 2, !args[1].hasPrefix("-") else {
    FileHandle.standardError.write("usage: ocr <image>\n".data(using: .utf8)!)
    exit(2)
}

let path = args[1]
guard let img = NSImage(contentsOfFile: path),
      let tiff = img.tiffRepresentation,
      let bmp = NSBitmapImageRep(data: tiff),
      let cg = bmp.cgImage else {
    FileHandle.standardError.write("cannot load image: \(path)\n".data(using: .utf8)!)
    exit(1)
}

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = false

do {
    try VNImageRequestHandler(cgImage: cg, options: [:]).perform([request])
} catch {
    FileHandle.standardError.write("ocr failed: \(error)\n".data(using: .utf8)!)
    exit(1)
}

for obs in request.results ?? [] {
    if let candidate = obs.topCandidates(1).first {
        print(candidate.string)
    }
}
