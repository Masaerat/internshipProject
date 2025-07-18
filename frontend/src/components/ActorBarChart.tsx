import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ReactECharts from 'echarts-for-react';
import { Spin, Alert } from 'antd';

interface ActorBarChartProps {
  rankMin: number;
  rankMax: number;
}

interface ActorData {
  actor: string;
  count: number;
}

const ActorBarChart: React.FC<ActorBarChartProps> = ({ rankMin, rankMax }) => {
  const [data, setData] = useState<ActorData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    axios
      .get('/api/actor-popularity', {
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

  const option = {
    title: {
      text: '演员热度TOP 20',
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params: any) => {
        const d = params[0].data;
        return `${d.name}<br/>出现次数: ${d.value}`;
      },
    },
    xAxis: {
      type: 'category',
      data: data.slice(0, 20).map((item) => item.actor),
      name: '演员',
      axisLabel: { rotate: 30 },
    },
    yAxis: {
      type: 'value',
      name: '出现次数',
    },
    series: [
      {
        data: data.slice(0, 20).map((item) => ({ name: item.actor, value: item.count })),
        type: 'bar',
        name: '热度',
        itemStyle: {
          color: '#5470C6',
        },
      },
    ],
  };

  if (loading) return <Spin tip="加载中..." />;
  if (error) return <Alert type="error" message={error} />;
  return <ReactECharts option={option} style={{ height: 400 }} />;
};

export default ActorBarChart;
