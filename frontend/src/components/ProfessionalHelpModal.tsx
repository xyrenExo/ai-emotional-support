"use client";

import React, { useEffect, useState } from "react";
import { Phone, MessageSquare, Globe, X, Loader2 } from "lucide-react";
import { chatAPI } from "@/lib/api";

interface ProfessionalHelpResource {
  country: string;
  country_code: string;
  crisis_hotline: string;
  crisis_number: string;
  crisis_text: string;
  therapist_directory: string;
  resources: string[];
  success?: boolean;
}

interface ProfessionalHelpModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const ProfessionalHelpModal: React.FC<ProfessionalHelpModalProps> = ({
  isOpen,
  onClose,
}) => {
  const [resources, setResources] = useState<ProfessionalHelpResource | null>(
    null,
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      fetchResources();
    }
  }, [isOpen]);

  const fetchResources = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await chatAPI.getProfessionalHelp();
      setResources(data);
    } catch (err) {
      setError("Unable to load professional help resources. Please try again.");
      console.error("Error fetching professional help resources:", err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-[#1A1A1A] border border-[#2A2A2A] rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="sticky top-0 bg-[#1A1A1A] border-b border-[#2A2A2A] p-6 flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-white">Professional Help</h2>
            <p className="text-sm text-gray-400 mt-1">
              Location-based mental health resources
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-[#252525] rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-6 h-6 animate-spin text-accent-500" />
            </div>
          ) : error ? (
            <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 text-red-400 text-sm">
              {error}
            </div>
          ) : resources ? (
            <div className="space-y-6">
              {/* Country Info */}
              <div className="bg-[#252525] rounded-lg p-4 border border-[#3A3A3A]">
                <div className="flex items-center gap-2 text-accent-400 mb-2">
                  <Globe className="w-4 h-4" />
                  <span className="text-sm font-medium">Location Detected</span>
                </div>
                <p className="text-lg font-semibold text-white">
                  {resources.country}
                  {resources.country_code !== "UNKNOWN" && (
                    <span className="text-gray-400 text-sm ml-2">
                      ({resources.country_code})
                    </span>
                  )}
                </p>
              </div>

              {/* Crisis Support */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Hotline */}
                <div className="bg-[#1A1A1A] border border-red-500/30 rounded-lg p-4 hover:border-red-500/50 transition-colors">
                  <div className="flex items-center gap-2 mb-3">
                    <Phone className="w-5 h-5 text-red-500" />
                    <h3 className="font-semibold text-white">Crisis Hotline</h3>
                  </div>
                  <p className="text-2xl font-bold text-red-500 mb-2">
                    {resources.crisis_number}
                  </p>
                  <p className="text-sm text-gray-400">
                    {resources.crisis_hotline}
                  </p>
                </div>

                {/* Text Support */}
                <div className="bg-[#1A1A1A] border border-accent-500/30 rounded-lg p-4 hover:border-accent-500/50 transition-colors">
                  <div className="flex items-center gap-2 mb-3">
                    <MessageSquare className="w-5 h-5 text-accent-500" />
                    <h3 className="font-semibold text-white">Text Support</h3>
                  </div>
                  <p className="text-sm text-gray-300 mb-2">
                    {resources.crisis_text}
                  </p>
                  <p className="text-xs text-gray-500">
                    Free and confidential support via text
                  </p>
                </div>
              </div>

              {/* Therapist Directory */}
              <div className="bg-[#252525] rounded-lg p-4 border border-[#3A3A3A]">
                <h3 className="font-semibold text-white mb-3">
                  Find a Therapist
                </h3>
                <a
                  href={resources.therapist_directory}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 bg-accent-500 hover:bg-accent-600 text-white px-4 py-2 rounded-lg transition-colors text-sm font-medium"
                >
                  Browse Therapist Directory
                  <Globe className="w-4 h-4" />
                </a>
              </div>

              {/* Additional Resources */}
              {resources.resources && resources.resources.length > 0 && (
                <div>
                  <h3 className="font-semibold text-white mb-3">
                    Local Resources
                  </h3>
                  <div className="space-y-2">
                    {resources.resources.map((resource, idx) => (
                      <div
                        key={idx}
                        className="bg-[#1A1A1A] border border-[#2A2A2A] rounded-lg p-3 hover:border-[#3A3A3A] transition-colors"
                      >
                        <p className="text-sm text-gray-300">{resource}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Important Note */}
              <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4">
                <p className="text-sm text-yellow-200">
                  <strong>Important:</strong> If you're in immediate danger or
                  having thoughts of self-harm, please contact emergency
                  services or the crisis hotline above immediately.
                </p>
              </div>
            </div>
          ) : null}
        </div>

        {/* Footer */}
        <div className="border-t border-[#2A2A2A] p-6 bg-[#0E0E0E]">
          <button
            onClick={onClose}
            className="w-full bg-[#2A2A2A] hover:bg-[#3A3A3A] text-white py-2 rounded-lg transition-colors font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProfessionalHelpModal;
