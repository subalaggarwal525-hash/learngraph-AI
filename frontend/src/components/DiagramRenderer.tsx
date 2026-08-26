import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';

interface DiagramRendererProps {
  specification: string;
  caption?: string;
  className?: string;
}

export const DiagramRenderer: React.FC<DiagramRendererProps> = ({
  specification,
  caption,
  className = '',
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [svgContent, setSvgContent] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    mermaid.initialize({
      startOnLoad: false,
      theme: 'dark',
      securityLevel: 'loose',
      fontFamily: 'Plus Jakarta Sans, sans-serif',
      themeVariables: {
        darkMode: true,
        background: '#090d16',
        primaryColor: '#6366f1',
        primaryTextColor: '#f8fafc',
        primaryBorderColor: '#4f46e5',
        lineColor: '#818cf8',
      },
    });

    const renderDiagram = async () => {
      try {
        setError(null);
        const uniqueId = `mermaid_${Math.random().toString(36).substr(2, 9)}`;
        const cleanSpec = specification.replace(/\\n/g, '\n').trim();
        const { svg } = await mermaid.render(uniqueId, cleanSpec);
        setSvgContent(svg);
      } catch (err: any) {
        setError('Diagram parsing preview');
      }
    };

    if (specification) renderDiagram();
  }, [specification]);

  return (
    <div className={`rounded-xl border border-slate-800 bg-slate-950 p-4 shadow-xl ${className}`}>
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5 mb-3 text-xs text-slate-400">
        <span className="font-semibold text-indigo-400 flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-full bg-indigo-500 animate-ping" />
          Structured Visual Model
        </span>
        <span className="text-[10px] bg-slate-900 px-2 py-0.5 rounded border border-slate-800 font-mono">
          Mermaid / SVG
        </span>
      </div>

      {error ? (
        <div className="p-4 rounded-lg bg-slate-900 text-xs font-mono text-slate-300 overflow-x-auto whitespace-pre">
          {specification}
        </div>
      ) : (
        <div
          ref={containerRef}
          className="overflow-x-auto flex justify-center py-2 diagram-container [&_svg]:max-w-full [&_svg]:h-auto"
          dangerouslySetInnerHTML={{ __html: svgContent }}
        />
      )}

      {caption && (
        <p className="mt-3 text-center text-xs text-slate-400 font-medium italic border-t border-slate-800/60 pt-2">
          {caption}
        </p>
      )}
    </div>
  );
};
