"use client";

import React from "react";
import { Music, Wind, Brain, Lightbulb, Phone, Volume2 } from "lucide-react";
import { FeatureToggles as FeatureTogglesType } from "@/types";

interface FeatureTogglesProps {
  features: FeatureTogglesType;
  onToggle: (feature: keyof FeatureTogglesType) => void;
}

const FeatureToggles: React.FC<FeatureTogglesProps> = ({
  features,
  onToggle,
}) => {
  const featuresList = [
    {
      key: "music" as const,
      icon: Music,
      label: "Music Suggestions",
      description: "Get calming music recommendations",
    },
    {
      key: "breathing" as const,
      icon: Wind,
      label: "Breathing Exercises",
      description: "Simple breathing techniques",
    },
    {
      key: "mental" as const,
      icon: Brain,
      label: "Mental Exercises",
      description: "Mindfulness activities",
    },
    {
      key: "insight" as const,
      icon: Lightbulb,
      label: "Mood Insights",
      description: "Understand your emotions",
    },
    {
      key: "professional_help" as const,
      icon: Phone,
      label: "Professional Help",
      description: "Crisis resources",
    },
  ];

  return (
    <div className="p-4 overflow-x-auto">
      <div className="flex space-x-3 min-w-max">
        {featuresList.map(({ key, icon: Icon, label, description }) => (
          <button
            key={key}
            onClick={() => onToggle(key)}
            className={`feature-toggle ${
              features[key] ? "feature-toggle-active" : ""
            }`}
            title={description}
          >
            <Icon
              className={`w-5 h-5 ${features[key] ? "text-calm-600" : "text-gray-400"}`}
            />
            <span
              className={`text-sm font-medium ${
                features[key]
                  ? "text-calm-700 dark:text-calm-300"
                  : "text-gray-600 dark:text-gray-400"
              }`}
            >
              {label}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default FeatureToggles;
