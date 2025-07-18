import React, { useState } from 'react';
import { Layout, Menu, InputNumber, Row, Col, message } from 'antd';
import {
  PieChartOutlined,
  GlobalOutlined,
  LineChartOutlined,
  DotChartOutlined,
  UserOutlined,
} from '@ant-design/icons';
import TypePieChart from './components/TypePieChart';
import RegionPieChart from './components/RegionPieChart';
import ReleaseLineChart from './components/ReleaseLineChart';
import ScoreScatterChart from './components/ScoreScatterChart';
import ActorBarChart from './components/ActorBarChart';

const { Header, Sider, Content } = Layout;

const menuItems = [
  { key: 'type', icon: <PieChartOutlined />, label: '类型分布' },
  { key: 'region', icon: <GlobalOutlined />, label: '地区分布' },
  { key: 'release', icon: <LineChartOutlined />, label: '上映时间分布' },
  { key: 'score', icon: <DotChartOutlined />, label: '评分分布' },
  { key: 'actor', icon: <UserOutlined />, label: '演员热度' },
];

const App: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [selectedMenu, setSelectedMenu] = useState('type');
  const [rankMin, setRankMin] = useState(1);
  const [rankMax, setRankMax] = useState(100);

  // 切换菜单
  const handleMenuClick = (e: any) => {
    setSelectedMenu(e.key);
  };

  // rank输入校验
  const handleRankChange = (type: 'min' | 'max', value: number | null) => {
    if (value === null) return;
    if (type === 'min') {
      if (value > rankMax) {
        message.error('最小rank不能大于最大rank');
        return;
      }
      setRankMin(value);
    } else {
      if (value < rankMin) {
        message.error('最大rank不能小于最小rank');
        return;
      }
      setRankMax(value);
    }
  };

  // 渲染内容区
  const renderContent = () => {
    switch (selectedMenu) {
      case 'type':
        return <TypePieChart rankMin={rankMin} rankMax={rankMax} />;
      case 'region':
        return <RegionPieChart rankMin={rankMin} rankMax={rankMax} />;
      case 'release':
        return <ReleaseLineChart rankMin={rankMin} rankMax={rankMax} />;
      case 'score':
        return <ScoreScatterChart rankMin={rankMin} rankMax={rankMax} />;
      case 'actor':
        return <ActorBarChart rankMin={rankMin} rankMax={rankMax} />;
      default:
        return null;
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div style={{ height: 32, margin: 16, color: '#fff', textAlign: 'center', fontWeight: 'bold' }}>
          豆瓣电影Hot100
        </div>
        <Menu theme="dark" mode="inline" selectedKeys={[selectedMenu]} onClick={handleMenuClick} items={menuItems} />
      </Sider>
      <Layout>
        <Header style={{ background: '#fff', padding: '0 24px' }}>
          <Row align="middle" gutter={16}>
            <Col>Rank范围：</Col>
            <Col>
              <InputNumber min={1} max={100} value={rankMin} onChange={v => handleRankChange('min', v)} />
            </Col>
            <Col>-</Col>
            <Col>
              <InputNumber min={1} max={100} value={rankMax} onChange={v => handleRankChange('max', v)} />
            </Col>
          </Row>
        </Header>
        <Content style={{ margin: '24px', background: '#fff', padding: 24, minHeight: 360 }}>
          {renderContent()}
        </Content>
      </Layout>
    </Layout>
  );
};

export default App;



// import React, { useState } from 'react';
// import './App.css';
//
// function App() {
//   const [input1, setInput1] = useState('');
//   const [input2, setInput2] = useState('');
//   const [input3, setInput3] = useState('');
//   const [response1, setResponse1] = useState('');
//   const [response2, setResponse2] = useState('');
//
//   // 第一个按钮的GET请求
//   const handleGetRequest = async () => {
//     try {
//       const response = await fetch(`/api/get-example?param=${encodeURIComponent(input1)}`);
//       const data = await response.text();
//       setResponse1(data);
//     } catch (error) {
//       console.error('Error:', error);
//       setResponse1('请求失败');
//     }
//   };
//
//   // 第二个按钮的POST请求
//   const handlePostRequest = async () => {
//     try {
//       const response = await fetch(`api/post-example?param=${encodeURIComponent(input3)}`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ bodyParam: input2 }),
//       });
//       const data = await response.text();
//       setResponse2(data);
//     } catch (error) {
//       console.error('Error:', error);
//       setResponse2('请求失败');
//     }
//   };
//
//   return (
//     <div className="App">
//       <header className="App-header">
//
//         {/* GET请求部分 */}
//         <div className="request-section">
//           <h2>GET请求示例</h2>
//           <input
//             type="text"
//             value={input1}
//             onChange={(e) => setInput1(e.target.value)}
//             placeholder="输入GET参数"
//           />
//           <button onClick={handleGetRequest}>发送GET请求</button>
//           <p>响应: {response1}</p>
//         </div>
//
//         {/* POST请求部分 */}
//         <div className="request-section">
//           <h2>POST请求示例</h2>
//           <input
//             type="text"
//             value={input2}
//             onChange={(e) => setInput2(e.target.value)}
//             placeholder="输入POST body参数"
//           />
//           <input
//             type="text"
//             value={input3}
//             onChange={(e) => setInput3(e.target.value)}
//             placeholder="输入POST URL参数"
//           />
//           <button onClick={handlePostRequest}>发送POST请求</button>
//           <p>响应: {response2}</p>
//         </div>
//       </header>
//     </div>
//   );
// }
//
// export default App;

