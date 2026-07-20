import AssetRiskCard from "./AssetRiskCard";
export default function RiskMap({ assets }) { return <section className="panel"><h2>Asset risk map</h2>{assets.map((asset) => <AssetRiskCard key={asset.id} asset={asset}/> )}</section>; }
