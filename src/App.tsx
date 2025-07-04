import React, { useState } from 'react';
import { User, Briefcase, MessageSquare, Target, Download, Linkedin } from 'lucide-react';
import ProfileAnalysis from './components/ProfileAnalysis';
import JobFitAnalysis from './components/JobFitAnalysis';
import ContentOptimization from './components/ContentOptimization';
import CareerGuidance from './components/CareerGuidance';
import ChatInterface from './components/ChatInterface';

type TabType = 'profile' | 'jobfit' | 'content' | 'career' | 'chat';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('profile');

  const tabs = [
    { id: 'profile' as TabType, label: 'Profile Analysis', icon: User },
    { id: 'jobfit' as TabType, label: 'Job Fit', icon: Briefcase },
    { id: 'content' as TabType, label: 'Content Optimization', icon: Target },
    { id: 'career' as TabType, label: 'Career Guidance', icon: Download },
    { id: 'chat' as TabType, label: 'AI Chat', icon: MessageSquare },
  ];

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'profile':
        return <ProfileAnalysis />;
      case 'jobfit':
        return <JobFitAnalysis />;
      case 'content':
        return <ContentOptimization />;
      case 'career':
        return <CareerGuidance />;
      case 'chat':
        return <ChatInterface />;
      default:
        return <ProfileAnalysis />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Linkedin className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">LinkedIn Profile Optimizer</h1>
                <p className="text-sm text-gray-500">AI-Powered Career Enhancement</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                NVIDIA AI Powered
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                FREE
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderActiveTab()}
      </main>
    </div>
  );
}

export default App;