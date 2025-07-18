import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ReactECharts from 'echarts-for-react';
import { Spin, Alert } from 'antd';

interface ScoreScatterChartProps {
  rankMin: number;
  rankMax: number;
}

interface ScoreData {
  title: string;
  release_date: string;
  score: number;
}

const ScoreScatterChart: React.FC<ScoreScatterChartProps> = ({ rankMin, rankMax }) => {
  const [data, setData] = useState<ScoreData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    axios
      .get('/api/score-distribution', {
        params: { rank_min: rankMin, rank_max: rankMax },
      })
      .then((res) => {
        if (res.data.success) {
          setData(res.data.data);
        } else {
          setError(res.data.msg || '数据获取失败');
        }
      })
      .catch((err) => {
        setError(err.message || '请求失败');
      })
      .finally(() => setLoading(false));
  }, [rankMin, rankMax]);

  // 解析年份
  const scatterData = data.map((item) => {
    let year = 0;
    try {
      year = parseInt(item.release_date.slice(0, 4));
    } catch {
      year = 0;
    }
    return [year, item.score, item.title];
  });

  const option = {
    title: {
      text: '评分分布',
      left: 'center',
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        const [year, score, title] = params.data;
        return `${title}<br/>年份: ${year}<br/>评分: ${score}`;
      },
    },
    xAxis: {
      type: 'value',
      name: '年份',
      min: (val: any) => val.min - 1,
      max: (val: any) => val.max + 1,
    },
    yAxis: {
      type: 'value',
      name: '评分',
      min: 0,
      max: 10,
    },
    series: [
      {
        symbolSize: 12,
        data: scatterData,
        type: 'scatter',
        name: '电影',
      },
    ],
  };

  if (loading) return <Spin tip="加载中..." />;
  if (error) return <Alert type="error" message={error} />;
  return <ReactECharts option={option} style={{ height: 400 }} />;
};

export default ScoreScatterChart;
